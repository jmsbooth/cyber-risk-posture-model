# CRPI prospective organizational study — outcome feasibility and freeze-decision record

**Decision status: UNRESOLVED. No primary endpoint, study horizon, sample size, normalizer, threshold or held-out analysis has been frozen.** The existing [metadata-only example](../config/prospective_pilot_registration.example.json) contains a **hypothetical** `independently_adjudicated_control_failure` and 28-day horizon; these are **not** approved study selections. The published CRPI scalar is an operational index, **not** a breach probability.

## A. Outcome eligibility and circularity screening

**Question:** Is the future outcome a service/time observation independently recorded from the CRPI inputs, with a reproducible adjudication rubric, adequate prevalence and a fixed follow-up window?

| Candidate future endpoint | Relative feasibility considerations | Primary threat to independent inference | Minimum acceptance before selection |
| --- | --- | --- | --- |
| Independently adjudicated **control failure** | May be sufficiently common in larger control-assurance programs; outcome naturally operational | Failure labels can be copied from `CM_verification`, `CM_integrity`, `SOE_detection` or training tests included in input evidence | Outcome test cohort, assessment staff and source stream distinct from scoring inputs; no case-by-case post hoc scoring changes |
| Cyber-attributed **service interruption** | Service telemetry and continuity owners may have documented impact duration | Broad operational downtime has non-cyber causes; cyber attribution is sparse, discretionary or delayed | Prespecified cyber attribution/case criteria, independent service telemetry, censoring and confounder plan |
| Independently adjudicated **security incident** | High conceptual relevance; can include defined severity | Low event prevalence, changing detection coverage, reporting bias; some source events drive both inputs and labels | Incident definition audited separately, enough independent cases/clusters and prospective follow-up |
| **Recovery exercise** result | Can be deliberately sampled and independently witnessed | Direct circularity with `RRAS_internal` exercise success and potential rehearsal leakage | Disjoint future exercises and independent assessors; no reuse of input-period exercise data or training scenarios; interpret as limited construct validation |
| Business **remediation deadline / assurance** outcome | Often measurable in issue trackers | Reuses `SOE_learning` actions or `RRAS_dependency` review processes; weak external construct validity | Distinct predeclared cases, times and adjudicators, plus reason why outcome is not merely the input re-expressed |

**Automatic outcome veto:** Reject an outcome if its label is derived from the same event, checklist, reviewer decision, exercise, control record or scoring calculation used as a CRPI primitive for the same or an improperly overlapping window. Independence requires *documented source/event separation*, not only differently named databases. Secondary/exploratory outcomes must be labeled as such.

## B. Candidate research estimands — not preregistered

1. **Measurement reliability (first-stage estimand):** For eligible, source-qualified `service × time` observations, assess concordance between two trained blinded reviewers calculating the 15 primitives and domain impact ratings. Report item-level coverage/denominator disagreement, repeatability and ordinal weighted agreement with uncertainty (including within-service clustering). A numerical score can be reproducible without measuring the intended construct.
2. **Incremental predictive discrimination/rank utility (conditional second stage):** On a prospectively untouched holdout, compare how well prior-window CRPI orders subsequent **independently adjudicated** outcomes relative to fixed baselines. Any chosen discrimination or association statistic must be prespecified as appropriate for an ordinal, binary, count or time-to-event endpoint; it does **not** make CRPI a probability estimator.
3. **Practical decision utility:** Evaluate a prespecified allocation/ranking decision under fixed review budget (e.g., ranking eligible service windows for subsequent independent audits) and analyze benefit/harms compared with cheaper measures. Never infer an optimal alert cutoff from the synthetic 0.15 test split.
4. **Sparse-data robustness:** Measure how often missingness stops a fully qualified CRPI and whether deterministic possible-value ranges remain decision-useful without false precision. Stratify missingness by cause and source, not only at random.

These are candidate estimands. A statistic and minimally meaningful difference should be frozen after a partner's data feasibility review **without examining prospective holdout labels**.

## C. Feasibility counts required before power/precision planning

Have the prospective partner's *authorized* analysts report only permitted, aggregate, nonidentifying feasibility metadata:

- Number of distinct eligible services and dependency clusters; exclusions, observed inventory coverage, and scope/date versioning.
- Planned measurement-window cadence and number of **independent** clusters (repeated windows are correlated, not independent organizations).
- Outcome frequency under a candidate independently adjudicated case definition and horizon; event denominator and follow-up losses **without providing case records in public**.
- Percentage of expected windows with all 15 usable primitives, p90 sample size and censoring; proportion of cold-start versus reconstructed stock.
- Degree of overlap between candidate outcome ascertainment and CRPI measurement sources; reviewer availability; data governance and privacy feasibility.
- Observed proportions at p90 normalization caps and in each 0–4 consequence level; major heterogeneity by service class and time.

**No numeric sample-size target is asserted.** A precision/power simulation may be designed in a private approved environment using reasonable, documented candidate prevalence, cluster correlations and effect sizes. It must not quietly treat weekly service windows as independent trials, manufacture positive cases, or fit to held-out outcomes. An 8–12-week schedule in the earlier draft is a **discussion example**, not a scientific adequacy claim.

## D. Fixed analysis and leakage controls

- `t0` is the time a scored observation is knowable. All raw evidence, source snapshots, review notes, profile selection and `S_previous` used for a score must be available **no later than `t0`**; delayed-arrival events need separately declared cutoff handling.
- Prospective outcome ascertainment starts **after `t0`**, in an explicitly locked interval `(t0,t0+h]`. Record censoring and unresolved cases; do not label incomplete follow-up as a negative.
- Use grouped service/dependency splits and time-forward holdout. Freeze assignment and an overlap/embargo rule before accessing holdout outcomes. Evaluate same eligible cases across CRPI and all baselines.
- Fit any data-derived normalizer, calibration mapping or optional probability link on training/calibration partitions alone; apply frozen transformations to the holdout. Report profile version and immutable digest.
- Compare `CRPI`, `R_inst`, the existing simple additive proxy, geometric-TE ablation and an evidence-only baseline. Keep a baseline's literal definition identical across evaluation sets; a different score magnitude is not automatically a better result.
- Preserve null/negative results. Account for service/dependency clustering in intervals and compare paired performance; predeclare multiplicity correction and practical effect size.
- Disclose denominator manipulation, source changes, monitoring coverage drift, rarity, missingness, first-time initialization and any exclusions. If an outcome has too few eligible independent observations to support its registered metric, report infeasibility rather than replacing the outcome after peeking.

## E. Required decision ledger before any study lock

| Decision | Current state | Required independent signoff/record |
| --- | --- | --- |
| Participating organization, permitted scope and study sponsor | **OPEN** | Organizational sponsor, owner authorization and selection-bias exclusion rationale |
| Data-use, confidentiality, human/ethics applicability | **OPEN** | Contract counsel/data custodian plus competent institutional ethics determination where applicable |
| 15-field numerator/denominator, ordinal anchors and time caps | **OPEN** | Source custodian + independent evidence auditor + blinded impact reviewers |
| Primary prospective outcome and study horizon | **OPEN** | Independent outcome adjudicator + statistical reviewer; circularity check |
| Sample size, cluster/time design and precision criteria | **OPEN** | Qualified statistician and signed assumptions |
| Grouped/forward holdout, embargo and leakage preflight | **OPEN** | Independent methodology review and recorded immutable plan |
| Versioned registration and private approvals | **OPEN** | Human governance signoff and time-stamped registration receipt; not just Git SHA |

After these decisions are reviewed, create an **organization-specific private registration** and preserve only metadata-only opaque references in the public validator. [OSF Registries](https://help.osf.io/article/770-registrations) is one possible platform for a time-stamped, potentially embargoed plan; no OSF registration is created by this repo or this document. Do not publish confidential appendices by accident.

### Decisions explicitly NOT taken by this packet

- No primary outcome or 28-day horizon frozen; no actual baseline is chosen as the winner.
- No consent, IRB determination, external validation, model calibration or incident prediction claim.
- No outside organization approached and no future data collection authorized.

Source of truth: [CRPI empirical-validation study protocol](EMPIRICAL_VALIDATION_STUDY_PROTOCOL.md) and [Issue #9](https://github.com/jmsbooth/cyber-risk-posture-model/issues/9).
