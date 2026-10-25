# CRPI field pilot — 15-input evidence and construct review charter (DRAFT)

**Status:** Field-review specification for **independent human review**. The 15 existing inputs and `config/measurement_pilot_v0.1.json` are **provisional**. This document proposes how to assess their actual semantic validity; it does not freeze calibration values, establish independent source integrity or change any CRPI equation.

**Unit of evidence:** a bounded `service_token × observation_window_end` with declared service/dependency scope, inventory snapshot and profile/version. Do not mix a corporation-wide ratio with a system-specific consequence rating without an explicit, reviewed translation. Original records and filled reviewer workpapers belong **only** in an approved private study workspace.

## A. Canonical input review inventory

`n/d` means a count ratio with an audited eligible population, nonzero denominator and frozen inclusion criteria. `k/4` maps one of five **ordinal** impact classes to a numeric placeholder but does **not** establish that neighboring classes are equal-interval. `inverse(hours; L,U)` is the pilot's clipped transformation `1 - clip((hours-L)/(U-L),0,1)`; its bounds are uncalibrated. The parent profile owns the exact methods and freshness parameters.

| Primitive | Existing pilot transform | Proposed source class and independent audit focus | Open construct threat |
| --- | --- | --- | --- |
| `TE_external` | risk, `n/d`; 7d freshness | Scoped internet-facing inventory + **validated actionable** exposure register; inspect both numerator and asset denominator snapshot | Added safe assets can lower ratio without reducing unsafe reachable paths; vulnerability severity and exploit preconditions omitted |
| `TE_internal` | risk, `n/d`; 30d | Identity/privilege graph, verified lateral-reachability path reviews and sampled negative paths | Assessment-only denominator is selected rather than exhaustively observed; graph path cardinality can explode |
| `CS_confidentiality` | risk, `k/4`; 180d | Data stewardship, contractual/regulatory impact and governed business-impact analysis | Impact tiers may not be equidistant; exposure to personal information requires independent privacy review |
| `CS_integrity` | risk, `k/4`; 180d | Business/mission owner scenarios, alteration/recovery impacts, independent consequence reviewers | Different service owners can interpret severity anchors inconsistently |
| `CS_availability` | risk, `k/4`; 180d | Service owner, continuity objectives and credible downtime scenarios | Same downtime can have nonlinear consequences by mission or season |
| `CM_coverage` | capacity, `n/d`; 7d | Required in-scope monitored control catalogue and monitoring configuration audit | Omitting unmonitored mandatory controls from denominator inflates apparent coverage |
| `CM_freshness` | capacity, inverse p90 hours; **L=0,U=24**, 7d, min **10** | Event/evidence pipeline timestamps with start/end clock definitions, clock skew and censoring flags | Small p90 sample/censoring, stale source snapshots and cap saturation |
| `CM_integrity` | capacity, `n/d`; 7d | Required evidence-stream inventory, independently reproducible provenance/integrity tests | Self-attestation of stream validity is not independent stream verification |
| `CM_verification` | capacity, `n/d`; 30d | Critical control inventory and objective control-state assessment artifacts | Same control test can be reused as monitoring and security-operation evidence |
| `USOM_detection` | capacity, `n/d`; 90d | Controlled detection exercise roster with attempted, missed and successfully triaged cases | Easy exercise selection and exclusions bias results; field incidents and rehearsals differ |
| `USOM_velocity` | capacity, inverse p90 hours; **L=0,U=72**, 90d, min **10** | Incident/exercise timelines with independently verified containment and event-start clocks | Inconsistent clock origin, unresolved cases, long-tail censoring and rehearsal bias |
| `USOM_change_safety` | capacity, `n/d`; 30d | In-scope change log with declared follow-up period, rollback and security regression evidence | Late adverse outcomes or changes lacking follow-up can be misclassified as safe |
| `USOM_learning` | capacity, `n/d`; 90d | Corrective-action ledger, due date baseline and independent effectiveness checks | Backlog aging, due-date manipulation and superficial closure |
| `RRAS_internal` | capacity, `n/d`; 180d | Recovery exercise plans, attempted objectives and independently observed outcomes | Exercise difficulty/coverage selection and same-case leakage to an outcome label |
| `RRAS_dependency` | capacity, `n/d`; 180d | Critical dependency inventory and independently reviewed assurance evidence | Documentary assurance is not demonstrated third-party operational resilience |

**A score that can be computed is not necessarily a valid measurement.** Reviewer certification must cover the construct, observational scope and denominator—not simply a successful schema parse.

## B. Per-field audit worksheet — to be completed privately

Create one private record *per field, service and measurement window*. Keep the public document unpopulated. Mandatory review columns:

| Column | Requirement |
| --- | --- |
| Scope and lineage | `study_id`, pseudonymous `scope_token`, `dependency_cluster_token`, `measurement_window_start/end`, model/measurement profile IDs and immutable profile hash |
| Construct definition | Primitive name, exact numerator and denominator or ordinal anchors, polarity, exclusions, units, eligible population and time boundary |
| Raw source | Private data-custodian identifier, opaque record reference, reproducible source digest, extraction time, inventory snapshot version and least-privilege access approval |
| Data quality | Eligible sampled count, denominator completeness, duplicates, zero versus missing, stale/late arrival, undetected/censored cases, reconciliation against an independent source |
| Review 1 and 2 | Two independent reviewer aliases, blinded rating/evidence check, timestamps, disagreement, adjudicator and reason; keep source independence explicit |
| Correctness qualification | `observed` / `unverifiable` / `not_applicable` / `missing` / `stale` / `insufficient_sample`, with reason and corrective action |
| Normalization | Pilot profile version, raw value, transform method, L/U or ordinal anchor ID, normalized numeric output, clipping status and sensitivity alternatives |
| Cross-construct reuse | `evidence_id` and list of all other constructs that reuse its records or control pathways; independent review disposition |
| Permission and publication | Private approval receipt, data-classification tag, allowed study uses and permitted derived outputs; **no private records in public Git** |

## C. Review criteria and explicit reasons to reject a point estimate

1. **Source authority:** Independent audit can reconstruct the numerator from authorized primary events and the denominator from a dated authoritative inventory. A named owner or `verified: true` alone fails this requirement.
2. **Scope/time equivalence:** The numerator, denominator, reviewer and asset/service boundary refer to the same `scope_token` and observation interval. No post-outcome leakage from future records into the earlier score.
3. **Directionality:** Higher TE/CS means greater risk; higher CM/USOM/RRAS means stronger monitoring/mitigation/resilience capacity. Reverse directions must not be silently reinterpreted.
4. **Censored and no-event distinction:** No eligible events for a p90 metric is **not zero hours**, and a zero denominator is **not perfect coverage**. Unresolved incidents remain eligible for separate censoring policy.
5. **Count validity:** Distinct identities/paths, stable enumeration, numerator subset of denominator, no hidden exclusion for failed or negative trials.
6. **Reviewer reliability:** Two *blinded* consequence ratings retained with source anchor; compare ordinal agreement (e.g., weighted kappa with a prespecified weighting) and report per-class confusion, prevalence and disagreements. Kappa does not prove the five levels have equal numeric spacing.
7. **Calibration uncertainty:** The current 24h/72h time caps, 10-case minimum and five-level ordinal spacing are **illustrative policies**, not empirically established thresholds or sample adequacy. Evaluate alternatives without tuning to prospective holdout outcomes.
8. **Cross-construct overlap:** Trace repeated `evidence_id` and common control mechanisms. The current pilot **reports** duplicate IDs but does **not** prohibit them or prove independence.
9. **Missingness governance:** Reject complete CRPI if a required input is missing/stale/unverified/undersampled. Allow a conditional *feasible-value interval* for instantaneous residual only; never present it as a statistical confidence interval or a complete temporal score.
10. **Reproducibility:** Re-run the frozen profile against an independently selected slice. Require reviewer-recorded explanations of any discrepancy; prohibit retrospective silent denominator changes.

## D. Proposed independent review sequence

- **Stage 1 — Dry-run, zero private ingestion:** Study lead selects candidate definitions and sample windows; domain experts inspect **this public template** only and record suggested replacements separately.
- **Stage 2 — Approved private source reconnaissance:** After formal authorization, source custodians verify feasible inventory snapshots, counts, event clocks and outcome-independent evidence sources **inside the approved environment**.
- **Stage 3 — Independent rubric and denominator audit:** Two qualified reviewers assess blinded copies. Freeze inclusion criteria, measured units, norm mapping, sample eligibility and repeated-record policy in a named pilot profile before held-out scoring.
- **Stage 4 — Locked evaluation:** Use frozen measurement profile and source/exclusion policy for study windows. Preserve original raw lineage privately and a cryptographic digest of *nonsensitive* specification metadata.
- **Stage 5 — Disagreement analysis:** Report reviewer agreement, missingness, cap saturation, selection bias and audit-failure rates **before** interpreting CRPI-outcome association.

A reviewer may approve *source availability* but reject *construct validity*. These are distinct decisions. Where one of the 15 provisional measures is infeasible, explicitly mark that field and assess partial-data coverage; do not fabricate evidence to force complete scores.

## External methodological anchors

- [NIST SP 800-55 Vol. 1: Identifying and Selecting Measures](https://csrc.nist.gov/pubs/sp/800/55/v1/final), December 2024.
- [NIST SP 800-55 Vol. 2: Developing an Information Security Measurement Program](https://csrc.nist.gov/pubs/sp/800/55/v2/final), December 2024.
- [NIST SP 800-53A Rev. 5: Security and Privacy Control Assessment Procedures](https://csrc.nist.gov/pubs/sp/800/53/a/r5/final). These materials inform audit design, **not** empirical acceptance of CRPI's 15 proxies.

See [pilot measurement profile](../config/measurement_pilot_v0.1.json), [current input contract](CRPI_OPERATIONAL_INPUT_CONTRACT.md) and [Issue #9](https://github.com/jmsbooth/cyber-risk-posture-model/issues/9).
