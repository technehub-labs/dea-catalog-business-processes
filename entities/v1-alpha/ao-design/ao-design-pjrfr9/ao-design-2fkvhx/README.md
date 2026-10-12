# Design Regulated Role Architecture

**id:** `processes:process-ao-design-2fkvhx`
**type:** BusinessProcess
**version:** 1.0.0
**admitted by:** CR-BP-106 (carrier for 5-cell A&O regulator-tied admission tranche)
**discovery record:** `dea:discovery-agency-and-organization-design-escape` (CR-BP-105 / PR #155)

## What this BP is

Design Regulated Role Architecture is the regulator-tied specialization admitted at the
**AgencyAndOrganization x Design** ECF coordinate. It was admitted as the
canonical decomposition for this cell because the substrate-neutral general-case BP
is insufficient on its own: regulator-licensed roles require a distinct governed
workflow with regulator-controlled scope, fitness-and-propriety attestation,
supervised-training completion, and continuing-supervisor notification.

## Trigger and outcome

- **Trigger:** The enterprise's role catalogue and competency framework include roles whose holders must hold regulator-issued licences or admissions, and the design must align each role's authority, signing capacity, and scope to the regulator's continuing-supervision framework before the role enters Build or Activate.
- **Outcome:** The role catalogue carries regulator-tied role entries; each licensed-role entry is aligned to its regulator's continuing-supervision framework, its competency and fitness-and-propriety attestation regime is documented, and the role is ready to enter Build and Activate stages without re-scoping.

## Evidence anchors

- (regulation) https://www.handbook.fca.org.uk/handbook/SYSC/25/Annex1/
- (regulation) https://www.ecfr.gov/current/title-14/chapter-I/subchapter-F/part-121/subpart-Y
- (regulation) https://eur-lex.europa.eu/eli/reg/2024/1689/oj
- (standard) https://www.jointcommission.org/en-us/standards/
- (standard) https://content.naic.org/cipr-topics/producer-licensing-model-act
- (standard) https://www.sra.org.uk/solicitors/standards-regulations/

## Adjacent contexts

This BP lives within the AgencyAndOrganization x Design cell. The
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
