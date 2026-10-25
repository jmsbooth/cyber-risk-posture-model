# CRPI prospective field pilot — participation brief (discussion draft)

**Status:** Invitation to discuss a future study; **not an enrollment offer, data-use agreement, preregistration, study approval, or validated risk assessment**. No organization is enrolled. Refer to [Issue #9](https://github.com/jmsbooth/cyber-risk-posture-model/issues/9).

## Purpose

Cyber Risk Posture Index (CRPI) is a decomposable index describing operational cyber exposure, potential consequences, monitoring, security operations and resilience, with an explicitly modeled persistent state. Its current [41-page mathematical paper](../paper/build/CRM_revised.pdf), conditional formal checks and synthetic tests do **not** establish predictive validity or measure breach probabilities. The next study asks a narrower and falsifiable question:

> Can independent reviewers produce comparable CRPI inputs from the same auditable organizational evidence, and do those measurements explain or discriminate later independently adjudicated operational outcomes better than prespecified simpler alternatives?

We seek **voluntary, authorized organizational collaboration** to determine whether a study is feasible. Expressions of interest alone are not authorization to access systems or collect evidence.

## Illustrative participation, subject to written approval

| Workstream | Potential participant contribution | Research deliverable |
| --- | --- | --- |
| Scope | Identify eligible business services, boundaries and accountable owners | A frozen service/dependency population and exclusion log |
| Evidence | Identify *available* source systems for the 15 provisional input primitives; specify numerator/denominator provenance and timestamps | Measurement feasibility and missingness audit, not silently imputed scores |
| Review | Nominate independent evidence/impact reviewers and a separate outcome adjudication role | Inter-rater reliability and documented disagreements |
| Outcome | Identify a subsequent operational outcome independently sourced from CRPI's input measures | Prospective outcome definition, eligibility and censoring plan |
| Governance | Obtain organization-approved data-use/retention controls and the appropriate ethics determination | Authorized private study workspace and immutable preregistration receipt |

The research protocol discusses repeated service-time observations (for example, weekly windows over 8–12 weeks as a **feasibility illustration only**). **No study duration, sample count, incident quota, score threshold or effect size is fixed**. Feasibility/power calculations must be grounded in the candidate organization's actual service count and independently observed outcome frequency *before* a prospective study begins.

## Privacy and data handling

- Participants remain the authority for their data and must approve the specific processing, storage, access, transfer, retention, disposal, permitted publication and breach-notification terms in writing.
- Real inventories, IP addresses, vulnerability cases, tickets, identity records, staff names, incident reports, event logs and other nonpublic data **must not enter this public GitHub repository or this ChatGPT conversation**. A private, organization-approved workspace is a prerequisite.
- Publish only descriptions and derived findings specifically cleared for release. Public synthetic fixtures never imply actual participant data.
- Prefer organization-local processing with pseudonymous service tokens, separation of reviewer and outcome roles, least-privilege research access, and independently logged evidence provenance. These are proposed controls, not assertions that a private environment exists.
- A participation agreement and legal/ethics review are required as applicable. IRB/human-subjects applicability is a matter for qualified institutional officials, not this project or a Python preflight.
- A participant may reasonably require that no per-service CRPI values or comparative rankings leave its own environment. Agree the scope of publications **before** data collection.

## What collaboration can produce

Subject to the agreed protocol and lawful release terms: an operational metric-definition audit, observed-data completeness and reliability findings, assessment of normalization assumptions, documented limitations and prospective comparison with stateless/additive/evidence-only baselines. **There is no promised favorable result, risk reduction, certification, compliance determination, or statistical significance.** Null results are an acceptable research outcome.

## Suggested initial feasibility meeting (without sharing evidence)

1. Confirm a named organizational sponsor with authority to initiate a *discussion* and a legal/data-governance contact.
2. Identify broad service classes and approximate available time windows **without providing records or identifiers**.
3. Identify which of the 15 input families have accessible, reviewable evidence and whether historical state reconstruction is plausible.
4. Determine whether a separate adjudicated future outcome is feasible without overlap with CRPI inputs.
5. Decide whether to proceed to an organization-led privacy/ethics assessment, data-use negotiation, source-definition workshop and power/precision feasibility assessment.

### Optional unsent introduction text

> I am developing a research study to test whether a mathematically defined cyber posture index can be measured consistently from real operational evidence, and whether it adds useful information beyond simpler baselines. I am looking for an organization willing to discuss a privacy-preserving feasibility pilot. The first conversation would cover potential service scope, available evidence categories, independent outcome review and governance requirements—no internal data would be requested until approved agreements and controls are in place. Would your security measurement and data governance leads be open to an initial discussion?

This text is **a template only**. It has not been sent, and no organization or contact has been selected.

## Research references

- [CRPI prospective validation research protocol](EMPIRICAL_VALIDATION_STUDY_PROTOCOL.md)
- [Prospective study readiness pack](PROSPECTIVE_PILOT_STARTER_PACK.md)
- [NIST SP 800-55 Vol. 1](https://csrc.nist.gov/pubs/sp/800/55/v1/final) and [Vol. 2](https://csrc.nist.gov/pubs/sp/800/55/v2/final) (December 2024): measurement selection and program governance, **not endorsement of CRPI**
- [HHS OHRP guidance on research and human-subjects determinations](https://www.hhs.gov/ohrp/coded-private-information-or-biospecimens-used-research.html): applicability requires fact-specific review
