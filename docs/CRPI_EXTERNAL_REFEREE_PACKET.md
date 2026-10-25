# CRPI — independent pre-submission referee packet

**Manuscript:** *A Dynamic, Decomposable Operational Cyber Risk Posture Index* — James Booth  
**Research edition:** 41 pages; repository baseline `0ed3d9ef9ab52627068abeccebf100b58dc4e308` (2026-10-25).  
**Purpose:** solicit **independent substantive critique**, not endorsements, institutional approval or declarations of empirically validated cyber risk.

## Review materials

- [Full research PDF](../paper/build/CRM_revised.pdf) and [LaTeX manuscript](../paper/CRM_revised.tex).
- [Mathematical verification coverage matrix](../verification/PROOF_COVERAGE_MATRIX.md) and [formal theorem sources](../formal/lean/README.md).
- [Numerical conformance record](../verification/PHASE_D_STATUS.md) and [synthetic stress results](../verification/STRESS_TEST_REPORT.md).
- [Illustrative measurement profile and constraints](../docs/CRPI_OPERATIONAL_INPUT_CONTRACT.md) and [prospective empirical validation protocol](../docs/EMPIRICAL_VALIDATION_STUDY_PROTOCOL.md).
- [Publication QA receipt](../verification/PUBLICATION_PDF_QA_PR7.md); it describes a previously verified PDF, not an independent certification by the referee.

## Precise claims under review

1. CRPI is a **bounded, decomposable operational posture index**, *not* a calibrated probability, loss frequency, monetary-loss prediction or control-assurance guarantee.
2. The model defines normalized observability (CM), consequence severity (CS), threat exposure (TE), unified security operations (USOM) and resilience (RRAS) constructs, combining them through declared weights and assumptions.
3. Hazard pressure is \(H=TE D_{eff}\), with consequence-specific resilience applicability; mitigation is \(M=USOM[m_0+(1-m_0)CM]\); instantaneous residual posture is \(R_{inst}=H(1-M)\).
4. A bounded unresolved-exposure stock obeys \(\\dot S=\\beta R_{inst}(1-S)-\\kappa MS\) and is exactly updated on piecewise-constant intervals; the reported index is the maximum of current residual and stock.
5. Six analytical propositions cover boundedness, directionality and fixed-input temporal behavior. Selected subclaims are machine checked under explicit premises, and synthetic tests demonstrate implementation behavior.
6. No collected organizational data, prospectively independent outcomes, calibrated threshold or demonstrated real-world decision utility is part of this paper.

## Suggested referee questions

**Mathematics / formal methods**
- Do the stated six propositions follow from the declared assumptions? Which claims are analytic only, conditional in Lean, or outside the machine-checked proof?
- Is the regularized geometric operator appropriate for the proposed construct semantics, including zero, tiny weights, sensitivity to \(\\varepsilon\), and weak-link behavior?
- Does the stock-flow formulation have sound initialization, identifiability, unit-of-time and nonconstant-input handling? What counterexamples test cadence, time aggregation and sequence sensitivity?
- Does the maximum envelope encode an explicit normative/conservative policy choice rather than a claimed natural risk law? Are switch behavior and gradient limitations correctly described?

**Cyber-risk, measurement, and construct validity**
- Are the five Tier-2 constructs meaningfully distinguishable? Could shared evidence or control effects be counted twice, particularly between observability, operational effectiveness and resilience?
- What makes multiplication \(TE\\,D_{eff}\) and \(USOM[m_0+(1-m_0)CM]\) preferable to comparably simple additive/multiplicative alternatives? What would falsify that preference?
- Can relative posture interpretations survive plausible reweighting, missingness, scope changes, changing denominator composition and calibration-profile shifts?
- Are novelty claims properly positioned versus Bayesian/attack-graph approaches, CVSS/EPSS/KEV, FAIR and recent dynamic-risk systems? What is genuinely new, and what is a formal combination of established components?

**Statistical and research-methods**
- Are all synthetic input distributions and priors explicitly described as invented? Are the sample design, test selection and comparison criteria reproducible and nonselective?
- Do the stress cases illustrate risk-model failure modes rather than prove performance superiority? What additional negative controls or ablations could be completed without empirical organizational records?
- Is the proposed prospective field study designed to avoid circular outcomes, dependent-sample leakage, outcome-driven normalizer tuning and overinterpreted confidence intervals?
- Which prospective outcomes and minimum precision criteria would be needed to substantiate operational value, and which of those belong in a *separate paper*?

## Structured review return form

For each concern supply: **ID**, **manuscript section/page**, **severity** (blocking / major / minor), **claim or assumption challenged**, **counterexample or independent evidence**, **requested change**, and **recommended disposition** (accept / revise / reject claim). Comments may be delivered privately rather than posted publicly.

Please also answer:
- **Technical correctness:** accept / needs revision / cannot assess, with premises.
- **Novelty positioning:** persuasive / incomplete / overlapping, with closest relevant work.
- **Reproducibility:** satisfactory from examined material / requires more artifacts / not attempted.
- **Scope language:** accurate / overclaims, with exact proposed edits.
- **Fit for external scholarly submission:** ready / major revision / not ready, and suggested venue *type*.

A favorable review **does not** establish empirical validity or guarantee acceptance by a journal, conference, or preprint server.

## Author response and change-control record

| Review ID | Reviewer expertise (anonymized) | Location | Severity | Requested change | Response and evidence | Revised commit | Resolution |
| --- | --- | --- | --- | --- | --- | --- | --- |
| *Pending* | *Not assigned* | — | — | — | — | — | Open |

No referee has been recruited or responded as of this packet's creation. The author should confirm any individual invitations or external distribution and keep reviewer identities/contact details out of public artifacts unless consented.

**Related:** [Publication readiness assessment](CRPI_PUBLICATION_READINESS_REVIEW.md), [external review Issue #12](https://github.com/jmsbooth/cyber-risk-posture-model/issues/12), [separate empirical pilot Issue #9](https://github.com/jmsbooth/cyber-risk-posture-model/issues/9).
