# CRPI prospective pilot — organization governance, private workspace and authorization gates

**Status:** Design/negotiation checklist **only**; no participant authorization, hosted workspace, processing agreement, ethics/IRB finding or data collection is represented as complete.

This packet documents what an organization would need to approve before any **nonpublic** security evidence is processed. It is **not a signed legal agreement** or opinion on whether human-subjects regulation applies. Organization counsel, privacy staff, risk owner and the responsible research/ethics official must determine and approve the actual conditions.

## 1. Roles and separation of duties

| Study role | Required responsibility | Separation rule |
| --- | --- | --- |
| Organizational sponsor | Authorizes consideration, business service scope and operational impact; names accountable contacts privately | Sponsor interest is **not** data access authority or researcher approval |
| Data custodian / security owner | Approves classified sources, permitted access, lawful purpose, retention, extraction and audit | No transfer until the data-use terms and workspace are approved |
| Inventory/source auditor | Reconciles numerators, denominators, timestamps and source provenance independently of score preparation | Must not rubber-stamp the same source owner's unsupported attestation |
| Measurement reviewers (two for consequence) | Independently assess 0–4 impact anchors and sample raw-to-normalized transformations | Blinded to combined CRPI/outcome where possible; retain both ratings before adjudication |
| Outcome adjudicator | Uses prespecified **independent** evidence and time horizons to determine later outcomes | Must not see the CRPI score or derive labels from input-period evidence |
| Statistician / methodology lead | Finalizes cluster/time holdout, power/precision, analytic metrics, missingness and correction | Frozen prospective design before viewing held-out labels |
| Governance/ethics authority | Determines applicable human-subjects, legal and contract obligations and approves conduct | Neither a GitHub reviewer nor the metadata validator can substitute for this authority |
| Research lead | Implements the frozen protocol, ensures provenance, logs deviations and reports null/negative findings | No self-issued approval that bypasses organizational or independent signoff |

For a small pilot, individuals may hold more than one administrative role where permitted, but **independence of source auditing, impact review and outcome labeling is a research design constraint**. Declare unavoidable overlap and assess how it weakens the claim rather than implying blinded independent review.

## 2. Private workspace minimum controls — required before first real evidence

1. **Custody and environment:** Confirm the organization-approved legal entity, tenant/location, data classes, authorized processors and private storage boundaries. Prefer study execution within the data-owning organization's environment. No private source data in public GitHub, issue comments, LLM chat text, unconstrained email or personal cloud storage.
2. **Approved source scope:** Inventory allowed systems and extracts, fields and identity attributes, collection purpose, named collectors, read-only permissions and use restrictions. Security telemetry may contain host identifiers, sensitive vulnerability knowledge and personnel data.
3. **Identity and segregation:** Require assigned named users/service identities, least privilege, MFA when available, explicit approval for access, segregated reviewer/outcome datasets, private join keys and audit logs. Reviewer aliases and pseudonymous service tokens must not make a reversible key publicly accessible.
4. **Integrity and immutability:** Record private raw-source version, event snapshot timestamp, source digest and evidence identifier. Hashes cannot establish that an original source was correct, only that its recorded bytes match a retained version. Keep immutable audit trails and separately controlled changes to profile/registration.
5. **Safe computation:** Run the existing CRPI raw-evidence adapter locally in the permitted private environment; keep input/source records and output-level service scores private unless specifically approved. Store the unchanged profile hash and all measurement lineage.
6. **Prohibited leakage:** Prevent future outcome labels, previously unseen audit findings and unblinded reviewer ratings from influencing input normalization, calibration, feature exclusions or time-series cold starts. Holdout access rules must be verified before scoring.
7. **Handling and retention:** Agree data minimization, encryption requirements, backup locations, incident notification, subcontractor permissions, retention period, withdrawal rights, deletion/audit evidence and permitted derived-result export. Values are subject to legal and organizational review; none are preapproved here.
8. **Release governance:** Before any paper/post, have the participating organization review proposed quotations, small-cell aggregate disclosure, reconstructed service identity risk and allowed outputs. Only publish consented nonsensitive aggregate and methodological artifacts.
9. **Revocation:** Explicit participant/organization termination and breach escalation path. Stopping access must stop new data ingestion and follow the agreed retention/deletion exceptions. No claim of unconditional data erasure if applicable records must be retained by law.
10. **Ethics/legal determination:** Obtain documented institutional determination of whether 45 CFR 46 or another applicable regime covers the study, especially if employee/analyst interviews or identifiable private information are processed. Do not unilaterally designate the study “IRB exempt”; if no IRB is required, retain the reasoned determination by a competent authority.

A public `.gitignore` pattern is only an accidental-commit guard, not an enforceable confidentiality or security control.

## 3. Agreement schedule — counsel-review outline (not binding)

An actual organization-specific data-use/participation instrument should specify the following, **without inserting real contact or infrastructure identifiers in public Git**.

| Schedule | Required negotiated content |
| --- | --- |
| Purpose and permitted processing | CRPI measurement research question, approved service classes, allowed data fields, precise study period, prohibited secondary use, and who directs processing |
| Roles and legal basis | Organizational authority, authorized researchers, privacy/ethics determination, role of human reviewers and third parties; participant consent if required by the applicable basis |
| Security and storage | Private environment owner, geographic/tenant constraints, IAM, encryption, access audit, approved transfer channels, security incident process |
| Independent measurement | Source inventories, denominator certification, correction procedure, dual impact ratings, sample-censoring and reviewer access controls |
| Outcome and holdout | Independent outcome adjudication, blinding, future window, case definitions, allowed case records, embargo and preregistration freeze |
| Retention and exit | Data retention/disposal, requested withdrawal/stop conditions, backups, return/delete certification, obligations that lawfully survive study closure |
| Publication/IP | Limits on publishing service-level scores, trade secrets and metadata, review period, attribution, veto/approval scope; no guaranteed favorable results |
| Responsibility and escalation | Decision rights, service owner, source auditor, research lead, organizational privacy officer, legal counsel and incident escalation chain |

The data custodian can approve *a technical data extract* only after organizational permission, source scope and purpose have been authorized; an engineer's access to a source does not itself grant study rights.

## 4. Linking approvals to the existing metadata preflight

The current [registration template](../config/prospective_pilot_registration.example.json) and [checker](../scripts/check_pilot_readiness.py) require 26 documentary/scientific conditions, including `governance.participant_consent_status`, `organizational_data_use_status`, `ethics_status`, `private_storage_attested`, 15-field definitions, outcome blinding, split freeze and preregistration receipts.

- **Before negotiation:** Use the *unapproved example unchanged*. Its normal validator returns structural validity but **26 pending gates**. `--require-ready` exits **2**, intentionally.
- **During negotiation:** Keep draft agreements, reviewer appointments and source inventories privately. A future study-specific metadata manifest may reference only approved opaque receipt IDs; **never fill the public example with actual contacts or private source references**.
- **After internal human approvals:** An approved governance official separately confirms that each receipt exists and is in force in the private workspace. A `documentary_gates_complete: true` result is merely **self-attested metadata consistency**, not actual authorization or scientific validation. `study_authorized_or_empirically_validated` correctly remains `false` in the public tooling.
- **Before held-out data:** Freeze source definitions, profile version, independent outcome, analyst split, prereg receipt and deviation log *before* inspecting prospective outcome labels.
- **After collection:** Independently audit data quality and statistical inference, report both favorable and null/negative results. Obtain publication clearance before releasing any derived statistics.

### External authority for oversight — not a legal determination

HHS OHRP's guidance on [coded private information](https://www.hhs.gov/ohrp/coded-private-information-or-biospecimens-used-research.html) explains that whether an activity involves human subjects depends on what investigators obtain and whether identities are readily ascertainable. HHS also distinguishes quality improvement from research designed to produce generalizable knowledge. Applicability to this particular cyber measurement protocol must be decided by the responsible institution and counsel. The public project's status cannot decide it.

See [participation brief](PILOT_PARTICIPATION_BRIEF.md), [15-input measurement review](PILOT_15_INPUT_FIELD_AUDIT.md), [outcome feasibility decision](PILOT_OUTCOME_FEASIBILITY_DECISION.md) and [Issue #9](https://github.com/jmsbooth/cyber-risk-posture-model/issues/9).
