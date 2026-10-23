# CRPI synthetic pressure test, operational failure analysis

**Execution:** Deterministic Python standard-library model evaluation matching the published CRPI equations. Fixed seed `20261023`, `N=12,000` independently sampled 15-value input configurations, with parameter settings from `config/calibration_baseline.json` (`illustrative-v0.1`). These are **mathematical/semantic tests**; they are not samples from actual organizations, incident outcome data, measured breach probabilities or a fit-for-use assessment.

**Execution provenance:** The initial 12,000-draw run and five regression checks were executed in an isolated Python 3.13.5 environment using a **source-faithful extracted copy of the published core formula functions**, with the complete `illustrative-v0.1` JSON calibration profile verified byte-for-byte against `main`. This environment could not clone GitHub because DNS/network access was unavailable. The committed reproduction script imports the **actual** `models.crm_reference` when run from the repository. Its exact-source replay on the owner's checkout is a separate **open acceptance gate**, not a pass inferred from mathematical similarity.

**Reproduce:** `python scripts/run_stress_tests.py --check verification/stress_test_results.json` and `python -m unittest discover -v` from repository root. Run with `--output verification/stress_test_results.json` to regenerate fixed results. The source-to-number receipt is `verification/stress_test_results.json` with seed and profile SHA-256. The code uses `models.crm_reference` and Python standard library only; no R dependency or SciPy installation is required.


**Original isolated equation-harness receipt (before the cross-platform hash repair):** Python 3.13.5; script SHA-256 `1069247cae9cad77ab8484937ad53edce6fd5e70d185823e2fd6d6cd312cfe6a`, fixed output SHA-256 `bba484de1516fd2a4accace9bee839a55a3cceebfe33a6388813304858e229b3`, exact illustrative calibration profile SHA-256 `7a8230e405f7ea2dab262d19781ba23c6f035d945f97bb9c81ee18c0d4daa447`. Regeneration comparison PASS and 5/5 stress-specific local tests PASS. These hashes attest this experiment, not the prior Lean kernel checks or publication PDF.

## Cross-platform reproducibility correction (2026-10-23)

The owner executed PR #7 on Windows with **Python 3.11.15**. The original `python -m unittest discover -v` run passed 23/24 tests; its sole failure was the exact JSON archive equality check, and `--check` reported a mismatch. The original stress runner computed `profile_sha256` from raw `calibration_baseline.json` file bytes, even though Git checkouts can contain either LF or CRLF line endings. The archived output was generated with Linux LF content.

This platform dependence was independently reproduced by copying the identical 2,777-byte calibration content into a CRLF version. Under identical synthetic draws and mathematical functions, the complete generated reports agreed except for **one metadata field**:

- LF profile hash: `7a8230e405f7ea2dab262d19781ba23c6f035d945f97bb9c81ee18c0d4daa447` (matches the archive).
- CRLF profile hash: `de85cd87d5d571412b41a6b40c0f4c54be1126c70f6e1647d3e962305078d995`.

The runner now loads the JSON profile in universal-newline text mode and hashes its normalized UTF-8 content. The input values, random generator, equations, archived statistical results and comparison tolerances are **unchanged**. A new test `test_calibration_hash_is_independent_of_checkout_line_endings` writes both LF and CRLF profile files and verifies equivalent results and equal hashes. The exact `--check` remains strict; if it still fails, it now identifies the differing top-level JSON fields instead of issuing an opaque message.

**Revalidation:** An isolated Python 3.13.5 reproduction using the source-faithful core formula copy reproduced all archived 12,000-draw data and passed **6/6 stress tests**, including the two-line-ending regression. The user's exact Windows checkout has **not yet been rerun after this fix**. Do not mark cross-platform acceptance complete until that run succeeds. The previously reported mathematical findings are unchanged by this platform metadata repair.

## Design and results

The input generator draws each normalized primitive **independently from Beta(2,2)**, deliberately creating a broad synthetic interior distribution, not a realistic population. In the boundedness/envelope check only, initial stock is independently Uniform(0,1). No organizations, cyber telemetry, threats or actual outcomes were sampled. Every statistic below is conditional on that constructed sampling design.

**Sanity checks:** 0/12,000 out-of-range output states. Median instantaneous residual was **0.1198** and its synthetic 90th percentile **0.2154**. With independent Uniform initial stock, the persistence stock controlled the single-step max envelope in **87.0%** of rows. The stock-dominance figure is strongly dependent on the *artificial initial stock distribution* and should never be generalized to deployed organizations.

### Missing-evidence experiments

For each synthetic row, randomly hide inputs, fill the missing values with 0.5 for a deliberately simple *counterfactual neutral-imputation* point estimate, and separately calculate feasible **mathematical** lower and upper residual bounds by assigning missing inputs the most/least risk-increasing admissible endpoints (zero or one). Monotonicity of the composed residual, under this profile, permits such a deterministic interval. The true synthetic complete-input residual is inside the interval in all 36,000 tested cases. This is a **possible-value interval**, not a confidence or credible interval.

Three mechanisms were evaluated: (a) 10% missing completely at random (MCAR) per field; (b) 20% MCAR; and (c) risk-correlated omission using 4% background missingness plus elevated omission probability when external threat is high, availability consequence is high or detection capability is weak. The last is an adversarial *scenario design*, not evidence that real telemetry has that missingness distribution.

| Missingness mechanism | Observed input mean | Median residual bound width | 90th %ile bound width | Intervals crossing illustrative 0.15 threshold | True positive cases missed by neutral fill |
| --- | ---: | ---: | ---: | ---: | ---: |
| 10% MCAR | 90.1% | 0.0487 | 0.2101 | 37.0% | 10.8% |
| 20% MCAR | 80.0% | 0.1387 | 0.3429 | 64.0% | 18.5% |
| Risk-correlated omission | 93.1% | 0.0289 | 0.1946 | 29.7% | 21.0% |

The 0.15 cutoff is **illustrative only**, with no security/operational calibration. “Missed” means a truly synthetic `R_inst >= 0.15` was pushed below 0.15 by neutral imputation; the percentages are conditional on those positive cases. Despite more observed fields, risk-correlated omission produced a negative mean signed bias of **−0.0090**, rather than the near-zero signed bias of MCAR. The *number of observed fields alone* is therefore not a reliable validation of the point estimate.

At 20% per-field MCAR, only **3.18%** of the 12,000 draws had all 15 primitives present. A reference runner that rejects any missing required field is mathematically safe but often cannot compute a complete scalar. Its operational interface should report valid partial components and missing evidence rather than produce fictitious precision. The current evidence gate checks five Tier-2 and per-domain coverage values *provided by the caller*; it is not a defensible substitute for source-verified normalization and missingness diagnostics.

### Parameter, temporal and interpretive experiments

| Test | Results | Operational interpretation |
| --- | --- | --- |
| Governed consequence weights | Moving `v=(1/3,1/3,1/3)` to `(0.6,0.2,0.2)` reversed **10.48%** of 6,000 independent pairwise residual rankings. Median absolute individual residual change **0.0167** (90th percentile **0.0474**). | Organization/scope rankings are profile-dependent. Do not compare scores as if weights and domain meanings were universal. |
| Regularization weak-link response | For `x=(0,0.8), w=(0.5,0.5)`, `G_epsilon` is **0.0273** at epsilon 0.001, **0.1592** at 0.05, **0.2813** at 0.25, and **0.3915** at 0.9. | Epsilon strongly controls how much weak components penalize the aggregate. It is a construct parameter to govern, not a “neutral” numerical constant. |
| Cadence with fixed inputs | Seven one-day stock transitions agree with the single seven-day exact transition to machine precision. | The proved fixed-input semigroup behaves correctly. |
| Time-varying week | Two high-residual/low-mitigation days and five recovery days, with fixed daily rates, produce stock **0.0302** if high-risk days occur first and **0.3794** if they occur last. A weekly average-input update reports **0.1383** for either ordering. | Losing the **order** of intra-week events can cause a large semantic error despite identical weekly means and a correct fixed-input cadence identity. The worst difference from the weekly average was **0.2411** in this deliberately extreme toy case. |
| Missing historical stock | With observed `R_inst=0.05`, `M=0.20`, true initial `S=0.85` vs neutral initialized `S=0.05`: day 1 envelope **0.7273** vs **0.0557**; day 7 **0.3102** vs **0.0752**. | Cold-start is an assumption about unavailable history; it should never be presented as a verified absence of inherited exposure. |
| Residual scalar nonidentifiability | `(H=0.4,M=0.5)` and `(H=0.8,M=0.75)` both yield `R_inst=0.2`; from the same prior stock 0.3, next stocks differ **0.2375** vs **0.1990**. | CRPI/residual alone does not reveal risk mechanisms. Always report `H`, `M`, and `S` separately. |
| Envelope masking | From prior `S=0.9` and `M=0.6`, increasing residual **0.1→0.3** changes the resulting envelope only **0.5639→0.5776**. | The persistent-state branch deliberately dampens instantaneous changes; dashboards need to expose current and historical contributions rather than overinterpret a nearly stable maximum. |

## Operational failure modes identified

The synthetic evidence supports four **conditions for safe implementation**, not claims that the model is empirically validated:

1. **Coverage must qualify rather than silently rescue absent measurements.** The existing missing-input rejection is a prudent executable default. A usable UI should additionally display partial results and admissible bounds under explicit `[0,1]` assumptions. Replacing absent values with 0.5 is not a universally defensible policy.
2. **Profile changes are semantic changes.** Weights, regularization, resilience applicability, normalized bounds and rates must be versioned, with “before/after recalculated on the same profile” distinguished from environmental change.
3. **Preserve the time ordering and prior state.** Fixed-input cadence consistency does not authorize averaging time-varying threat and mitigation over long intervals. Cold-start flags and temporal-history quality must accompany CRPI.
4. **Never publish CRPI as a lone score.** At least `R_inst`, `S`, `H`, `M`, `D_eff`, `TE`, source coverage and active max branch are needed for a defensible decision trace.

## What is not established

The sample independence, Beta(2,2) marginals, Uniform stock, illustrative 0.15 threshold, omission probabilities, high/low week and alternative weights are **analyst-selected mathematical probes**. They do not estimate real event rates, security efficacy, score distribution, population false-negative rates, or statistical confidence in any actual organization. Monte Carlo percentages are descriptive of the **synthetic test design only**. This work does not establish optimal `beta`, `kappa`, `m0`, epsilon, `rho`, any normalized raw evidence mapping, observational validity, or predictive superiority.

**Next scientific study:** Run a shadow-mode pilot using governed evidence mappings from real systems, compare CRPI trends and decomposition against operational outcomes and a simpler additive baseline, and test temporal/profile stability. That study is separate from the completed bounded mathematical verification and this synthetic stress-test phase.