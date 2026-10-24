# CRPI prospective measurement and external-validity research protocol

**Research-stage protocol (not a study result).** This protocol proposes how to determine whether normalized CRPI evidence actually tracks useful organizational security properties. It does not authorize collecting identifiable personal data, proprietary incident records or client data without appropriate approvals and data-governance controls.

## Question and null hypotheses

**Primary measurement question:** Can two trained reviewers derive comparable normalized primitive inputs from the same independently audited source evidence, within the same declared scope/profile/time boundary?

**Primary outcome question:** Does an evidence-qualified time series of CRPI provide incremental *explanatory or discriminative* value for subsequent independently adjudicated operational outcomes beyond simpler, predeclared baseline indicators? CRPI remains an index, not a breach probability.

Null hypotheses for review: (1) inter-rater agreement is no better than a practical naive baseline; (2) governed calibration is unstable across scoped business units or time; (3) CRPI adds no holdout value over a stateless instantaneous residual or a simple additive evidence index; (4) partial-evidence qualification does not adequately distinguish uncertain score ranges. None has been evaluated here.

## Pilot population, consent and scope

Select a bounded, consenting pilot set of independent *systems/business services* with explicit ownership. For each service, record asset/identity/dependency boundaries, impact domains, environment, inventory snapshot time, assessment reviewers and profile version. Begin with more than one type of service to expose sensitivity to unequal domain consequence, exposure and observability patterns. **Do not assert a fixed required sample size** without a prevalence/power assessment based on candidate outcomes; a small exploratory pilot cannot establish a generalizable model.

Collect repeated time windows (e.g. weekly operational measurements for 8–12 weeks as an *example*, not a requirement), retain the actual observation timestamp and change-event order, and use a finer cadence for known bursts. Freeze definitions and profile versions before scoring each holdout interval.

Suggested independently adjudicated outcomes, subject to eligibility and availability: material incident occurrence, severity on a predeclared ordinal rubric, realized service interruption duration, verified control failures, remediation backlog aging and validated recovery test outcomes. **An observed incident label or forward window must never be defined directly from the same CRPI inputs**, or the apparent performance would be circular. No score threshold is operationally validated by the synthetic research.

## Evidence intake and reliability gates

- Require scoped primary source records, immutable or reconstructable inventory denominators, source owner, collection timestamp, review timestamp, freshness policy and tested semantic mapping for every measured primitive.
- Distinguish no-event from missing-data. A zero denominator means *not evaluable*, not automatic full performance. A supplier assurance document or control checkbox is not itself a successful incident response or recovery exercise.
- Dual-review the ordinal consequence ratings while blinded to the final CRPI score, and retain both ratings and adjudication rationale. Estimate weighted agreement or another appropriate ordinal reliability measure and report the number of disagreements and disagreements by domain. Do not assume 0–4 rubric levels are empirically equal-distance impact units.
- Audit random and high-consequence source slices against authoritative inventories and raw tickets: numerator/denominator accuracy, event-duration definitions, nonreporting bias, stale data, unverifiable flags and inconsistent ownership.
- Track data missing *by cause* (missing at random, missing due to control absence, not applicable, lack of incident sample, outage, untrusted evidence) rather than adopting neutral filling as default. Compare complete-case, interval and explicitly governed estimation policies, labeling each as such.
- Preserve time-ordered trajectories, lineage and cold-start flags. A score with guessed initial stock is not equivalent to one with independently reconstructed historical state.

## Calibration controls

Before any fitting, preregister a limited set of candidate mappings for every field: raw units, numerator/denominator, lower/upper bound `L/U` or ordinal anchors, expected cadence, eligible sample size, direction and allowed transformations. Use a **named pilot measurement profile** separate from the paper's existing illustrative calibration profile. Estimate normalizer bounds from a training subset and evaluate their stability under perturbations; do not tune against the withheld outcome labels, target-looking numeric cutoffs, or published synthetic examples.

Organizational weights, epsilon, `m0`, beta, kappa, resilience-applicability and temporal priors should remain explicitly governed. Parameter changes should be justified by measurement construct semantics or independently measured data rather than by optimizing the display score. A domain weight change can reverse rankings without invalidating the equations. Hold out distinct system clusters and later time windows to reduce correlated leakage. Record the exact normalization/profile SHA and when it took effect.

## Predeclared baselines and analysis

All comparisons must operate on the **same scoped rows, timestamps and eligibility population**; note that raw score *magnitudes* are not comparable across indices with different mathematical semantics.

1. **Stateless residual** `R_inst`: remove the stock history and compare against CRPI to test whether persistence adds incremental description of later *independent* events and control/recovery results.
2. **Simple additive operational index** `(TE + D_eff + (1 - M)) / 3`: a deliberately non-mechanistic, normalized comparator, not the same quantity as CRPI. Report rank discordance and outcome-relevant paired diagnostics rather than interpreting a higher/lower absolute value as more valid.
3. **Geometric-ablation model:** replace the regularized geometric TE primitive aggregation with the same weighted arithmetic TE, while retaining all other paths. This isolates one modeling choice.
4. **No-model/evidence-only baselines:** audited high-severity unresolved exposure count, response-age quantile, or structured subject-matter expert tier when available, with denominators governed and reviewers blinded.

The source repo contains executable *synthetic* examples for baseline items 1–3. They measure **structural ranking disagreement only**, not predictive validity. For prospective real outcomes, report concordance/rank association (confidence intervals accounting for clustered service/time observations) and calibrated association models only where interpretation supports it. If predicting truly binary prospective outcomes becomes an explicitly separate research task, fit an independent probability link on training data and evaluate probability calibration and Brier/log loss **for that fitted probabilistic model**, never directly for an uncalibrated CRPI index.

Use time-split and system-split holdouts, and account for repeated measures within a service or dependency cluster. Include uncertainty intervals via cluster bootstrap or a comparable resampling method, preregister correction for multiple comparisons where necessary, and report absolute performance and whether the incremental improvement is operationally meaningful. Consider negative controls, drift by business unit and profile, sensitivity to data withholding, and the consequences of deliberately sparse or manipulated numerator/denominator inventories.

## Data governance, publication and go/no-go gate

- Retain confidential ticket details, inventory and people-level identifiers exclusively within the participating organization's approved environment; publish only permitted derived anonymized statistics or synthetic fixtures. Do not commit customer/source snapshots, names, credentials or original incident records to this public repo.
- Require participating owner agreement and a data retention/withdrawal plan. An ethics/IRB determination should be sought where applicable to the human review and research design.
- Model outputs must include source scope, calibration/measurement profile identifier, normalized input lineage, coverage quality, missingness and possible intervals, initialized vs inherited stock, and exact time units.
- Reject a “validated CRPI” claim until measurement reliability, independent outcomes, holds-out evaluation, baseline comparisons, and reproducibility all pass stated, precommitted acceptance criteria. It is legitimate for the prospective study to show that a simple index performs as well as CRPI or that a parameter choice is unidentifiable; report those findings.
- A separate writeup should distinguish *validity of measurement*, *mathematical correctness*, *numerical implementation conformance*, and *outcome utility* rather than using “validated” as a single label.

References for measurement-program design: [NIST SP 800-55 Vol. 1](https://doi.org/10.6028/NIST.SP.800-55v1) and [Vol. 2](https://doi.org/10.6028/NIST.SP.800-55v2) (December 2024). These publications guide measure selection and governance, not validation of the specific CRPI pilot proxy choices.