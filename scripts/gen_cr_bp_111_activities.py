#!/usr/bin/env python3
"""CR-BP-111 L3 Activity generator for the 5 A&O regulator-tied BPs from CR-BP-106.

Produces 4 Activity records per BP (5 BPs x 4 = 20 Activities). Each Activity
follows the established pattern (4 concerns per cell: supervisor-controlled scope,
fitness-and-propriety, supervised-training completion, continuing-supervisor
notification) drawn from the BP's own description/outcome text per the L3
deposition procedure.

Run: python3 scripts/gen_cr_bp_111_activities.py
"""
import os
import sys
from pathlib import Path

# 5 BPs from CR-BP-106 (cell -> BP path -> 4 activity decompositions)
CELLS = {
    'ao-conceive': {
        'bp_id': 'processes:process-ao-conceive-pnrhem',
        'bp_slug': 'ao-conceive-pnrhem',
        'bp_name': 'Conceive Licensed or Regulated Agent Capacity',
        'parent_group_hash': 'ao-conceive-bwjhgd',
        'domain': 'AgencyAndOrganization',
        'stage': 'Conceive',
        'identifier': 'ecf:agencyOrganization.conceive',
        'activities': [
            ('ao-conceive-cqkwrm', 'Declare Regulator-Licensed Role Mix',
             'Declare the regulator-licensed role mix on the regulated personnel record: count and category of regulator-licensed roles, the regulator-tied scope of each, and the alignment between the regulated personnel record and the regulator continuing-supervision framework. Shared concern: regulated-scope declaration. Input: the enterprise agent-capacity strategy; the regulator licensing taxonomy. Output: the committed regulated-scope declaration.'),
            ('ao-conceive-vnkqzf', 'Document Fitness-And-Propriety Attestation Regime',
             'Document the fitness-and-propriety attestation regime that will apply to each regulator-licensed role: the attestation form (initial, periodic, event-driven), the attestor (candidate, employer, regulator), and the regulator framing (SMCR FIT; state healthcare CME; bar MCLE; NAIC CE; FAA recurrent). Shared concern: fitness-and-propriety regime declaration. Input: the regulator licensing taxonomy; the attestation regime matrix. Output: the documented fitness-and-propriety attestation regime on the regulated personnel record.'),
            ('ao-conceive-fmxtqr', 'Map Supervised-Training Completion Requirements',
             'Map the supervised-training completion requirements for each regulator-licensed role: the training plan, the supervised-completion evidence class, and the regulator recording path (SMCR Statement of Responsibilities; state healthcare CE; NAIC CE; FAA / EASA type-rating; SRA Continuing Competence; bar MCLE). Shared concern: supervised-training mapping. Input: the regulator licensing taxonomy; the supervised-training matrix. Output: the mapped supervised-training completion requirements.'),
            ('ao-conceive-pzmwkl', 'Capture Continuing-Supervisor Notification Path',
             'Capture the continuing-supervisor notification path for each regulator-licensed role: the supervisor identity, the notification cadence, the notification content (SMCR Conduct Rules; fitness attestations; training completions), and the escalation matrix. Shared concern: continuing-supervisor notification path. Input: the regulator licensing taxonomy; the supervision matrix. Output: the captured continuing-supervisor notification path on the regulated personnel record.'),
        ],
    },
    'ao-design': {
        'bp_id': 'processes:process-ao-design-2fkvhx',
        'bp_slug': 'ao-design-2fkvhx',
        'bp_name': 'Design Regulated Role Architecture',
        'parent_group_hash': 'ao-design-pjrfr9',
        'domain': 'AgencyAndOrganization',
        'stage': 'Design',
        'identifier': 'ecf:agencyOrganization.design',
        'activities': [
            ('ao-design-jbf2v9', 'Catalogue Regulator-Tied Role Entries',
             'Catalogue the regulator-tied role entries in the role catalogue: each role authority, signing capacity, controlled-function designation (FCA SMCR CF1..CF11), the regulator licensing basis, and the regulator-tied scope of each. Shared concern: regulator-tied role catalogue. Input: the regulated-scope declaration; the role catalogue skeleton. Output: the regulator-tied role catalogue entries.'),
            ('ao-design-wnqz3k', 'Align Competency Framework To Continuing-Supervision',
             'Align the competency framework entries for each regulator-licensed role to the regulator continuing-supervision framework: the competency statements, the assessment cadence, the assessor (employer / regulator), and the alignment to the regulator continuing-competence program. Shared concern: competency-framework alignment. Input: the regulator-tied role catalogue; the competency framework skeleton. Output: the aligned competency framework entries.'),
            ('ao-design-x9k4m7', 'Define Fitness-And-Propriety Assessment Regime',
             'Define the fitness-and-propriety assessment regime for each regulator-licensed role: the assessment form (initial / annual / event-driven), the criteria, the attestor, and the regulator framing (SMCR FIT; state healthcare CME attestation; bar MCLE; NAIC CE; FAA recurrent). Shared concern: fitness-and-propriety assessment regime. Input: the regulator-tied role catalogue; the fitness-and-propriety matrix. Output: the defined fitness-and-propriety assessment regime.'),
            ('ao-design-v8r5n2', 'Define Continuing-Supervisor Notification Path',
             'Define the continuing-supervisor notification path for each regulator-licensed role: the supervisor identity, the notification cadence, the notification content, and the escalation matrix. Shared concern: continuing-supervisor notification path. Input: the regulator-tied role catalogue; the supervision matrix. Output: the defined continuing-supervisor notification path.'),
        ],
    },
    'ao-build': {
        'bp_id': 'processes:process-ao-build-9my4jr',
        'bp_slug': 'ao-build-9my4jr',
        'bp_name': 'Build Regulated Agent Pool',
        'parent_group_hash': 'ao-build-m6fmyx',
        'domain': 'AgencyAndOrganization',
        'stage': 'Build',
        'identifier': 'ecf:agencyOrganization.build',
        'activities': [
            ('ao-build-q7m3k9', 'Verify Candidates Against Regulator Licence Registry',
             'Verify each candidate against the regulator licence registry: FCA Financial Services Register; NMLS / NAIC Producer Database; FAA airmen certification database; US state bar admissions registries; state healthcare licensure registries (FSMB, Nursys, NABP, ARRT, ARDMS, NBRC). Shared concern: licence-registry verification. Input: the candidate list; the regulator registry access. Output: the verified-candidate list with the regulator licence record.'),
            ('ao-build-w2n8p4', 'Attest Fitness-And-Propriety For Pool',
             'Attest fitness-and-propriety for each candidate in the regulator-ready pool: the initial attestation, the attestor (employer / regulator), the criteria, and the regulator framing (SMCR FIT; state healthcare initial fitness; bar admissions fitness; NAIC producer fitness; FAA airmen fitness; EU AI Act Article 14). Shared concern: fitness-and-propriety attestation. Input: the verified-candidate list; the attestation regime. Output: the fitness-and-propriety attested candidate list.'),
            ('ao-build-f5k1m3', 'Screen Candidates Against Sanctions / AML / FCRA / ADA',
             'Screen each candidate against OFAC sanctions (31 CFR 501), Bank Secrecy Act AML / KYC (31 USC 5311), FCRA background (15 USC 1681), and ADA fitness (42 USC 12112). Shared concern: regulator-specific screening. Input: the fitness-attested candidate list; the screening matrix. Output: the screened candidate list with the sanctions / AML / FCRA / ADA clearances.'),
            ('ao-build-r6h2t8', 'Stage Regulated Personnel Record',
             'Stage the regulated personnel record for each cleared candidate: the supervisor-controlled scope, the fitness-and-propriety attestation, the supervised-training completion plan, the continuing-supervisor notification path, and the regulator-tied readiness for Activate. Shared concern: regulated personnel record staging. Input: the screened candidate list; the regulated personnel record schema. Output: the staged regulated personnel record ready for Activate.'),
        ],
    },
    'ao-operate': {
        'bp_id': 'processes:process-ao-operate-ba8scr',
        'bp_slug': 'ao-operate-ba8scr',
        'bp_name': 'Operate Regulated Performance Oversight',
        'parent_group_hash': 'ao-operate-35gmps',
        'domain': 'AgencyAndOrganization',
        'stage': 'Operate',
        'identifier': 'ecf:agencyOrganization.operate',
        'activities': [
            ('ao-operate-z4n9m2', 'Audit Conduct-Rule Compliance',
             'Audit regulator-licensed role conduct-rule compliance: FCA SMCR COCON (Conduct Rules); FINRA Rule 3110; FAA Part 117 (flight / duty time); EU AI Act Article 14 (human-oversight conduct); state bar professional conduct; state healthcare professional conduct. Shared concern: conduct-rule compliance audit. Input: the live regulator-licensed role list; the conduct-rule matrix. Output: the conduct-rule compliance audit record.'),
            ('ao-operate-j8k5p7', 'Annual Fitness-And-Propriety Re-Attestation',
             'Run the annual fitness-and-propriety re-attestation for each regulator-licensed role: SMCR FIT annual assessment under SYSC 25; state healthcare annual fitness; bar MCLE annual fitness; NAIC annual CE; FAA recurrent. Shared concern: annual fitness re-attestation. Input: the live role list; the annual attestation calendar. Output: the annual fitness re-attestation record.'),
            ('ao-operate-q3w6r1', 'Track Hours-Of-Work And Rest-Rule Compliance',
             'Track hours-of-work and rest-rule compliance for each regulator-licensed role: FAA Part 117 flight / duty / rest; state healthcare work-hour limits; SMCR fitness-and-propriety indicators; EU AI Act Article 14 oversight-hours. Shared concern: hours-of-work compliance. Input: the live role list; the hours-of-work recording. Output: the hours-of-work and rest-rule compliance record.'),
            ('ao-operate-b5v2k9', 'Track Continuing-Competence Completion',
             'Track continuing-competence completion for each regulator-licensed role: state bar MCLE; state healthcare CME; NAIC CE; FAA recurrent; EU AI Act Article 14 ongoing training. Shared concern: continuing-competence tracking. Input: the live role list; the continuing-competence plan. Output: the continuing-competence completion record.'),
        ],
    },
    'ao-improve': {
        'bp_id': 'processes:process-ao-improve-qqxe4d',
        'bp_slug': 'ao-improve-qqxe4d',
        'bp_name': 'Improve Regulated Workforce Capability',
        'parent_group_hash': 'ao-improve-su4c8p',
        'domain': 'AgencyAndOrganization',
        'stage': 'Improve',
        'identifier': 'ecf:agencyOrganization.improve',
        'activities': [
            ('ao-improve-x7m4n2', 'Run Regulator-Mandated Recurrent Training',
             'Run regulator-mandated recurrent training cycles: FCA SMCR fit-and-proper annual assessment (SYSC 25 / FIT); state bar MCLE; state healthcare CME; NAIC CE; FAA Part 121 subpart Y recurrent training; EU AI Act Article 14 ongoing training. Shared concern: recurrent training cycle. Input: the live role list; the regulator training matrix. Output: the recurrent training completion record.'),
            ('ao-improve-k9w5p8', 'Run Fit-And-Proper Re-Assessment Cycle',
             'Run the fit-and-proper re-assessment cycle for each regulator-licensed role: SMCR FIT annual re-assessment; state healthcare re-licensure; bar MCLE re-admission; NAIC license renewal; FAA airmen re-certification. Shared concern: fit-and-proper re-assessment. Input: the live role list; the re-assessment calendar. Output: the fit-and-proper re-assessment record.'),
            ('ao-improve-f2r6t4', 'Execute Regulator-Mandated Remediation',
             'Execute regulator-mandated remediation programs: regulator-supervised remediation (consent orders, undertakings, settlements); employer-driven remediation (performance plans, supervised practice). Shared concern: remediation program execution. Input: the remediation trigger; the remediation plan. Output: the remediation completion record.'),
            ('ao-improve-v3h8k1', 'Notify Continuing Supervisor Of Improvement',
             'Notify the continuing supervisor of each regulator-licensed role of the recorded improvement: the recurrent training completion, the fit-and-proper re-assessment, the remediation completion, and the regulator continuing-supervision framework status. Shared concern: supervisor notification of improvement. Input: the improvement record; the supervisor notification path. Output: the supervisor notification record.'),
        ],
    },
}


def make_activity_yaml(cell, slug, name, definition, cell_data):
    """Generate the Activity yaml content."""
    activity_id = f"processes:activity-{slug}"
    parent_group = cell_data['parent_group_hash']
    return f"""id: {activity_id}
type: Activity
name: {name}
version: 1.0.0
lifecycle_status: candidate
status: candidate
definition: 'The cohesive grouping of work within {cell_data["bp_name"]} that {definition}'
belongs_to_business_process: {cell_data['bp_id']}
cohesion_rationale: 'Cohesion score 9/9 assessed at deposition (CR-BP-32 section 6). Constituent work shares a single {name.lower()} concern, one input class, and one output (the {name.lower()} record on the regulated personnel record).'
decomposition_boundary: l4-reached
ecfConformance:
  framework: EnterpriseConceptFramework
  contractVersion: 1.0.0
  profile: dea:ecf@1.0.0
  status: conformant
  affiliation: inherits-catalog
  canonicalReferences:
  - kind: coordinate
    domain: {cell_data['domain']}
    stage: {cell_data['stage']}
    identifier: {cell_data['identifier']}
metadata:
  established_by: CR-BP-111
  established_at: '2026-10-12'
  change_history:
  - cr: CR-BP-111
    date: '2026-10-12'
    change: |
      Initial L3 Activity entry; lands as part of the CR-BP-111 L3
      decomposition tranche for the 5 ADMIT-CANONICAL A&O regulator-tied
      Business Processes (CR-BP-106). Classified per CR-BP-32 section 5
      (fails standalone executability and resource dedication);
      decomposition boundary marker per CR-BP-32 section 12 pending
      Task records (dea:Task lifecycle: proposed).
"""


def main():
    root = Path('entities/v1-alpha')
    n_act = 0
    for cell, data in CELLS.items():
        bp_dir = root / cell / data['parent_group_hash'] / data['bp_slug']
        for slug, name, definition in data['activities']:
            act_dir = bp_dir / slug
            act_dir.mkdir(parents=True, exist_ok=True)
            yaml_path = act_dir / f'processes-activity-{slug}.yaml'
            content = make_activity_yaml(cell, slug, name, definition, data)
            yaml_path.write_text(content)
            print(f'wrote: {yaml_path}')
            n_act += 1
    print(f'\nTotal Activity records written: {n_act}')


if __name__ == '__main__':
    main()
