# CRPI operational measurement pilot: raw-evidence contract, v0.1

**Status:** Executable *synthetic/pilot methodology*, **not an empirically calibrated score**. The governing CRPI equations, `config/calibration_baseline.json`, mathematical proofs and reference implementation are unchanged.

## Why this increment exists

The published CRPI paper defines 15 normalized primitives, but the original reference runner begins *after* raw evidence has already become a `[0,1]` score. The gap is a governed interface from observations to the 15 values, including provenance, denominator, freshness, missingness, and an explicit measurement rubric. This increment supplies a narrow demonstration adapter with a deliberately **provisional** pilot profile.

The measurement-design and governance methodology is consistent with NIST [SP 800-55 Volume 1 (identifying/selecting measures)](https://doi.org/10.6028/NIST.SP.800-55v1) and [Volume 2 (measurement-program governance)](https://doi.org/10.6028/NIST.SP.800-55v2). It does **not** claim NIST approves the selected scoring bounds or the CRPI model.

## Layered interface

```
Scoped inventory / telemetry / exercise and business-impact observations
  -> evidence entry: source_ref, unique evidence_id, scope_id, owner, observed_at, asserted verified
  -> governed pilot normalizer: fraction, ordinal 0..4, or bounded elapsed hours
  -> one normalized [0,1] primitive per eligible observation
  -> core CRPI model, unchanged: 5 Tier 2 constructs, D_j, R_j, D_eff, H, M, R_inst, S, CRPI
  -> qualified output: provenance, normalized lineage, missingness, coverage gate and
                       exact residual possible-value interval when inputs are missing
```

The source inventory and denominator are part of the model's *measurement boundary*, not independent truth certified by the adapter. The same ratio can change when an inventory expands, and unobserved assets can make an apparently high coverage ratio meaningless. Manual ordinal levels require a reviewer, a recorded assessment rationale, and a stable scope.

## Illustrative raw-to-normalized mapping

The configuration at [`config/measurement_pilot_v0.1.json`](../config/measurement_pilot_v0.1.json) is the executable source of all 15 starter field definitions, owners, freshness windows and (for time metrics) illustrative upper bounds. The 15-field mapping uses the **same primitive names and directions** as [`operational_input_contract_v1.json`](../config/operational_input_contract_v1.json).

| Field(s) | Raw evidence pilot method | Higher normalized score | Calibration limitation |
| --- | --- | --- | --- |
| `TE_external` | Count of verified actionable-exposure internet-facing systems / all in-scope internet-facing systems | More exposed | Exposure *count* is a crude substitute for severity, exploitability and reachable paths. Denominator must be audited. |
| `TE_internal` | Unsafe assessed privilege/attack paths / total paths independently assessed | More exposed | Discovery coverage, attacker reachability and identity privilege are not uniformly captured by simple path counts. |
| `CS_confidentiality`, `CS_integrity`, `CS_availability` | Ordinal 0–4 assessed consequence class; normalize to `level/4` | Greater inherent consequence | Five textual rubric anchors are **not** validated equal-interval utilities; inter-rater reliability and cross-domain comparability remain open. |
| `CM_coverage`, `CM_integrity`, `CM_verification` | Fraction of expected coverage/integrity/control-verification targets that pass tests | Stronger visibility | Inventory / test validity / source-reliability assumptions; never interpret uninstrumented sources as passing. |
| `CM_freshness` | P90 observed telemetry lag in hours, illustrative 0–24 cap | Fresher validated telemetry | A provisional cap and a minimum of 10 source observations are needed for this *demo*, not sufficient to prove a robust p90. |
| `USOM_detection`, `USOM_change_safety`, `USOM_learning` | Successful independently triaged exercises, safe verified changes, or due corrective-action closures / respective eligible denominators | Better operating capability | Exercise selection bias; no work due or no exercises yields **missing**, not an automatic 100%. |
| `USOM_velocity` | P90 verified time from trigger to containment, illustrative 0–72 hours | Faster containment | Must declare event start/stop semantics, censored cases and minimum 10 cases/exercises. No time observations means **missing**. |
| `RRAS_internal`, `RRAS_dependency` | Recovery objectives met / tested objectives; critical dependencies independently reviewed / declared critical dependencies | Stronger resilience and assurance | Outcome must be independently tested; supplier attestation alone is not verified survivability. |

For `fraction` inputs, `numerator` and `denominator` **must be integers with `0 <= n <= d` and `d > 0`**. For five-level ordinal inputs, only integer levels `0..4` are allowed. For `inverse_bounded_hours`, the normalized score is `1 - clip((hours-L)/(U-L),0,1)` with illustrative `L,U` and a minimum scenario sample size. The profile is not a claim that an hourly lag of 24 hours or 72 hours is a universally meaningful security boundary.

The above ratio proxies are proposed operational *candidates*, not validated measures or standards-driven definitions. They are not necessarily exhaustive or mutually independent. Reusing the same evidence ID across multiple constructs is **reported in `reused_evidence_ids`**, but is **not** automatically rejected and does not append a separate warning. Reviewers must inspect the reported duplicates and justify transformations that avoid counting the same control effect twice; this demo does not provide independent source de-duplication.

## Evidence eligibility and sparse evidence

Every supplied field is checked for matching `scope_id` and time-zone-aware `observed_at`, non-empty `source_ref`, `evidence_id`, and `owner`, caller-asserted `verified: true`, bounded raw values, no future timestamps, and profile-defined freshness windows. Missing, stale, unverified or undersampled observations are **ineligible** to produce a complete point score. A program can only check the declaration that a source was verified; it cannot independently authenticate a source or attest organizational inventory completeness.

The application produces **11 evidence-coverage paths**: five Tier 2 coverage fractions plus three consequence domain and three resilience-projection coverage fractions. These are derived from *usable primitive slots*, not the caller's arbitrary “coverage confidence” declaration. It then checks the reference profile's provisional aggregate/minimum/governing-path thresholds. Neither observed-score quality nor coverage is a probability of correctness.

If **any** required primitive is unavailable, the result includes `missing_required`, `evidence` reasons and a mathematically feasible *residual* interval. It computes the endpoints by filling unknown risk-direction primitives with `0`/`1` and unknown capacity-direction primitives with `1`/`0`, and reevaluating the canonical functions; no assumed joint probability is attached. It returns `point: null` and no CRPI, irrespective of how narrow the interval may look. This residual interval relies on the published coordinate-monotonicity under fixed profile assumptions; it does **not** include calibration or outcome uncertainty.

For all 15 usable primitives, it reports the canonical decomposed components (`TE`, `CS`, `CM`, `USOM`, `RRAS` reporting, `D_j`, `R_j`, `D_eff`, `H`, `M`, `R_inst`). A *temporal CRPI* additionally requires `prior_stock` with `dt_days`, or an explicitly declared `cold_start` that sets `S(t0) = R_inst(t0)` **without pretending to reconstruct history**. Without either, it reports an instantaneous decomposition, not a temporal score. Even a full-point output is labeled **synthetic_only** or **self_reported_provisional**, never empirically “verified.”

These are **provisional** governance rules; do not use them for funding priorities, regulatory decisions, supplier selection, inter-organizational league tables or automated high-stakes decisions before independent field validation.

## Run the fully fictional example

```bash
python scripts/run_operational_pilot.py \
    --input data/examples/operational_pilot_case.json \
    --output artifacts/pilot_evaluation.json
python scripts/compare_operational_baselines.py --check verification/measurement_pilot_structural_results.json
python -m unittest discover -v
```

The fixture contains invented counts, ordinal judgments, times, attestation flags and `prior_stock=0.4` for a fictional service. With the baseline illustrative model profile, its current instantaneous residual is `0.039969698`, but its carried stock yields `CRPI=0.239723943`; both are model-derived **fictional example outputs**, not measurements of any real entity. The fixture's coverage is `1.0` because every *fictional* primitive is supplied with an asserted verification flag, **not** because any organization has been verified.

## What must happen before organizational use

1. **Fix scope and denominator semantics:** stable asset inventory snapshot, system boundary, business function, critical dependency set, consequence exposure basis, pilot owner and observation clock.
2. **Review each of 15 measures:** classify observed vs inferred vs expert-rated; agree units, event start/stop definitions, source systems, eligibility denominators, test populations, domain allocation and freshness SLAs.
3. **Calibrate without leakage:** derive normalization anchors and weights only from declared calibration evidence, keep holdout systems/time windows blind, and preserve older profile IDs for longitudinal comparisons. Avoid selecting anchors that merely force a desirable output.
4. **Audit measurement reliability:** independent source-sample audit, business impact inter-rater agreement, drift, stale/invalid fraction, actual denominator reconciliation, and evidence double counting.
5. **Evaluate external utility:** prospective matched-scope time series, simple additive and stateless baselines, withheld outcomes, effect-size uncertainty, negative controls, and reporting of failure as well as success.
6. **Govern scale:** a system-level model is not an average of component CRPI values; derive the parent's consequence, exposure, dependency and evidence boundaries separately.

A preregistration-grade plan for step 5 is in [EMPIRICAL_VALIDATION_STUDY_PROTOCOL.md](EMPIRICAL_VALIDATION_STUDY_PROTOCOL.md). The [Windows 37-test acceptance and reviewer caveats](../verification/MEASUREMENT_PILOT_WINDOWS_ACCEPTANCE.md) qualify the provisional implementation. This repo **contains no private organizational records or incident labels** and therefore cannot yet claim any demonstrated empirical validity.