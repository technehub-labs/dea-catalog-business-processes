# Build Regulated Agent Pool

**id:** `processes:process-ao-build-9my4jr`
**type:** BusinessProcess
**version:** 1.0.0
**admitted by:** CR-BP-106 (carrier for 5-cell A&O regulator-tied admission tranche)
**discovery record:** `dea:discovery-agency-and-organization-build-escape` (CR-BP-105 / PR #155)

## What this BP is

Build Regulated Agent Pool is the regulator-tied specialization admitted at the
**AgencyAndOrganization x Build** ECF coordinate. It was admitted as the
canonical decomposition for this cell because the substrate-neutral general-case BP
is insufficient on its own: regulator-licensed roles require a distinct governed
workflow with regulator-controlled scope, fitness-and-propriety attestation,
supervised-training completion, and continuing-supervisor notification.

## Trigger and outcome

- **Trigger:** The enterprise is sourcing candidates for regulator-licensed roles whose qualifications must be verified against the regulator's licence registry and whose fitness-and-propriety must be attested before they enter the regulated personnel record, and the enterprise must apply regulator-specific screening (KYC, AML, sanctions, fitness declarations, FCRA-compliant background, ADA-compliant fitness) that differs from the substrate-neutral agent-acquisition flow.
- **Outcome:** The licensed-candidate pool is verified, cleared, and on the regulated personnel record; each candidate is fitness-and-propriety attested and ready for regulator-tied Activate without re-screening.

## Evidence anchors

- (regulation) https://www.register.fca.org.uk/
- (regulation) https://www.occ.treas.gov/topics/supervision-and-examination/aml/index.html
- (regulation) https://www.ecfr.gov/current/title-31/section-501.603
- (regulation) https://www.ecfr.gov/current/title-15/chapter-I/subchapter-C
- (regulation) https://www.ecfr.gov/current/title-29/subtitle-A/chapter-XIV
- (regulation) https://www.ecfr.gov/current/title-14/chapter-I/subchapter-F/part-61
- (standard) https://www.fincen.gov/resources/advisories-fact-sheets
- (standard) https://content.naic.org/cipr-topics/producer-licensing-model-act
- (regulation) https://eur-lex.europa.eu/eli/reg/2024/1689/oj
- (standard) https://www.finra.org/rules-guidance/rulebooks/finra-rules/3110

## Adjacent contexts

This BP lives within the AgencyAndOrganization x Build cell. The
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
