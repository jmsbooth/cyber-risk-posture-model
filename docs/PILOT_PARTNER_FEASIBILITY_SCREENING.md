# CRPI pilot partner — non-sensitive feasibility screening and onboarding decision log

**Status:** UNSENT / no candidate selected. This questionnaire is for a voluntary **pre-data** discussion; it must **not** request inventories, screenshots, incident examples, IPs, account identities, asset lists, employee names, regulated records or other security-sensitive source data. A sponsor should answer through an organization-approved channel, not by posting confidential responses to a public GitHub issue or chatbot.

## Stage A — Determine eligibility without collecting evidence

The following are **qualitative screening questions**, not permission to ingest data:

| # | Screening question | Suggested safe response |
| --- | --- | --- |
| 1 | Is an organizational sponsor willing to discuss a potential cyber-measurement research study? | Yes / no / pending; **do not publish sponsor identity** |
| 2 | Are service/system boundaries and accountable service owners defined? | Yes / partial / no |
| 3 | Are there multiple distinct service/dependency groups that could be eligible for independent evaluation? | Yes / no / unknown; no service names |
| 4 | Does the organization have *some* authoritative asset inventories and exposure-configuration evidence? | Yes / partial / no; no counts or host details needed |
| 5 | Is there a documented required-control and telemetry-stream catalogue? | Yes / partial / no |
| 6 | Are incident/exercise detection and containment clocks recorded, with attempted/missed cases retained? | Yes / partial / no; no cases supplied |
| 7 | Is there a governance process for independent business-impact assessment across confidentiality, integrity and availability? | Yes / partial / no |
| 8 | Are there independently witnessed recovery tests and a critical-dependency inventory? | Yes / partial / no |
| 9 | Can a *later* operational outcome be adjudicated independently, by a reviewer blinded to CRPI, from sources not reused as inputs? | Yes / uncertain / no |
| 10 | Is there a legal/privacy/research governance contact willing to review participation, data-use and human-subjects applicability? | Yes / no / pending |
| 11 | Could analysis run entirely in an approved organization-controlled environment with the study's source records remaining private? | Yes / partial / no |
| 12 | Is the organization prepared to accept a study that may find CRPI **no more useful** than a simple baseline, and to review permitted aggregate publication terms? | Yes / no / undecided |

No answer needs numerical detail during initial discovery. **Do not ask for credentials, customer data or operational examples.** A company with weak coverage is not automatically excluded; documented absence is a legitimate feasibility finding. However, an organization that cannot obtain valid authority or separate future outcome evidence cannot enter the proposed **prospective external-validity** design.

## Stage B — Internal partner qualification decision

After a consenting *discussion*, record only a protected internal decision (not in the public repository). This is a qualitative triage rather than an instrument score:

- **Decline/not feasible:** No authorized sponsor or no path to lawful governance/private custody; no independent outcome can be defined; no minimum source lineage.
- **Feasibility workshop only:** Some relevant inputs but major missing denominators, reviewer independence or prospective outcome uncertainty. No personal/incident records transferred; work first on approved source definitions.
- **Candidate subject to governance:** Sponsor and reviewers agree on a study concept. Next require independent source quality, documented permissions, private workspace and a locked protocol; **still not authorized**.
- **Eligible for authorized study only after human approvals:** The responsible organization documents access, ethics applicability, data-use and sampling decisions and separately releases use of its actual evidence. The public metadata checker alone **cannot** grant this decision.

## Stage C — Mandatory handoff before the first source record

1. Receive authorization through approved organizational governance and counsel, not merely research-email interest.
2. Agree a minimal, non-sensitive service/dependency scope and obtain a private list of eligible service tokens under the approved storage policy.
3. Complete the [15-input source/reviewer audit](PILOT_15_INPUT_FIELD_AUDIT.md) with authoritative denominator snapshots and normalization assumptions.
4. Select an [independent prospective outcome](PILOT_OUTCOME_FEASIBILITY_DECISION.md) only after prevalence/leakage feasibility review, and predeclare a realistic power/precision rationale.
5. Set up the [approved private workspace and participation schedule](PILOT_PRIVATE_WORKSPACE_AND_AUTHORIZATION.md).
6. Freeze an organization-specific preregistration and holdout analysis plan *before* any held-out outcome inspection; preserve external or independent timestamps and signoff.
7. Start permitted measurements under the approved scope. No service-level records or outcome data go into this public repository.

## Internal research decision ledger (blank on purpose)

| Decision | State as of drafting | Who must confirm |
| --- | --- | --- |
| Candidate organization and authorized sponsor | **UNSELECTED** | Organization's accountable security/business sponsor |
| Privacy/data-use and ethics determination | **NOT OBTAINED** | Qualified institution, counsel and governance official |
| Approved private study workspace | **NOT PROVISIONED OR VERIFIED** | Organization data custodian/security owner |
| 15-input field definitions, anchors and independent source audits | **UNREVIEWED** | Independent measurement reviewers and source custodians |
| Future outcome and holdout feasibility | **UNDECIDED** | Blind outcome adjudicator and statistician |
| Preregistration freeze and enrollment | **NOT DONE** | Approved governance authority / independent research lead |
| Source-data intake and empirical evaluation | **PROHIBITED UNTIL AUTHORIZED** | Designated research governance decision |

This is an unpopulated handoff artifact. It does not report any recruitment attempt or private facts about a prospective partner.

**Related:** [Participation brief](PILOT_PARTICIPATION_BRIEF.md), [parent Issue #9](https://github.com/jmsbooth/cyber-risk-posture-model/issues/9).
