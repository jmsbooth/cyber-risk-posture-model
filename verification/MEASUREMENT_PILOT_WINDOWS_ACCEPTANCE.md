# CRPI Operational Measurement Pilot — Exact-Checkout Acceptance and Scope Review

**Acceptance date:** 2026-10-24  
**Branch:** `research/crpi-operational-measurement-pilot`  
**Tested source head:** `9da4bb61995cc397d4a3f64d2464e5a6dc23f413`  
**Scope:** Source-matched **methodological pilot and synthetic reproducibility**, not organizational instrument validation.

## Owner-local Python evidence

The repository owner fetched and checked out the tracked research branch and ran the three acceptance commands from `E:\\personal\\_papers\\cyber-risk-posture-model`. The outputs below are taken from the owner's supplied PowerShell console, not from a GitHub Actions run or a signed external test attestation.

| Test | Reported result |
| --- | --- |
| `python scripts/run_operational_pilot.py --input data/examples/operational_pilot_case.json` | **PASS**, returned the full 15-field raw-to-normalized example, all five Tier-2 and six domain-coverage paths, lineage and complete decomposition |
| `python scripts/compare_operational_baselines.py --check verification/measurement_pilot_structural_results.json` | **`Pilot structural reproduction PASS`**; archived 600 synthetic scopes, 5,000 comparison pairs and structural statistics reproduced |
| `python -m unittest discover -v` | **`Ran 37 tests in 6.041s — OK`**: all 37 passed |
| New pilot-specific tests | **12/12 passed**: fixture/decomposition; missingness bounds; stale/false/future evidence handling; low-sample rejection; invalid fractions/ordinals; scope separation; rejected fabricated history; coverage without score scaling; denominator/bound sensitivity; deterministic and archived comparisons |
| Existing tests | All **25/25** previous tests passed; Phase D Decimal oracle again verified **44 fields** |

The printed synthetic fixture matches the independently retrieved repository artifact `verification/operational_pilot_example.json`: `R_inst=0.03996969804513359`, `S_next=CRPI=0.23972394314498544`, `TE=0.22387211655923572`, `D_eff=0.5476584498492331`, `M=0.6739973958333334`. Both report all 15 normalized synthetic observations present, prior-stock mode `supplied_prior_stock`, all evidence coverage paths `1.0`, and `status=synthetic_only`.

The reproduced structural output is stored as `verification/measurement_pilot_structural_results.json`. It reports **44.70%** CRPI-vs-stateless residual rank reversals, **43.92%** versus an additive proxy, and **0.28%** under an arithmetic-TE ablation across 5,000 generated comparison pairs. The data are deliberately synthetic with independently sampled prior stocks; these rates are **not** measures of prediction accuracy, generalizability, organizational risk, or model superiority.

## Methodological semantic review — research-only acceptance

The pilot raw-evidence proxy/profile definitions and the intake code were checked against the published operational-input contract and `models.crm_reference` path. The review found the following **explicit limitations** that must remain visible when considering an actual organization's measurement validity.

| Area | Finding / scope qualification | Required action before field-validity or production claim |
| --- | --- | --- |
| Exposure numerator and denominator | `TE_external` is a count ratio over declared internet-facing systems, not weighted exploitability or attack path reachability; `TE_internal` has an *assessed-only* denominator vulnerable to discovery/selection bias. A score can improve when denominator composition changes with no risk reduction. | Independent scope inventories, frozen denominator semantics and sensitivity to asset criticality/selection |
| Consequence rubric | Five ordinal consequence ratings are divided by four, implicitly treating successive classes as equally spaced and cross-domain comparable. | Independent blinded reviewers, inter-rater analysis, comparable outcome anchors or defensible ordinal modeling |
| Time quantiles | The p90 lag/containment proxies use arbitrary 24/72-hour illustrative caps and require only 10 samples. This is not sufficient to establish tail quantile reliability; censoring/long-tail incidents are not handled. | Establish event definitions, sample eligibility/power, censoring treatment, domain-specific calibration and uncertainty |
| Multiple use of evidence | Monitoring coverage, monitoring verification, and incident detection share potential control/evidence pathways; resilience exercise outcomes may also contribute to other constructs. The same evidence ID can appear more than once. | Independent source-lineage audit, deduplication/overlap governance, and tests for material double-counting |
| Evidence authenticity and coverage | `verified: true` is asserted by the caller; owner/source IDs and self-attested completeness are not authenticated, and a reused evidence ID is reported but not a rejection. A derived coverage value of 1.0 does **not** mean evidence is trustworthy or inventory complete. | Independent sample audit, owner and source authentication, denominator reconciliation, double-use controls |
| Missingness | If any of 15 required inputs are missing, stale or unverified, only a bounded feasible **instantaneous residual** interval is returned; no point CRPI. This interval holds measured inputs, weights, prior assumptions and normalizer policy fixed. | Study partial-evidence usability; do not portray the interval as statistical confidence or a full temporal risk bound |
| Temporal stock and baseline tests | Synthetic `S_0` and rates have no organizational calibration; large rank reversals vs stateless residual follow partly from independently invented prior stocks. | Independently reconstruct state history, record cadence, compare against outcomes and simpler baselines in time-separated holdout |

**Result:** No contradiction of the core CRPI equation, primitive direction, or existing formal proofs was identified in the reviewed pilot mapping. The proxy choice, interval assumptions, conditional independence, denominator design and calibration are **not** scientifically validated by a method/code desk review. This is a **research-methodology acceptance**, not an independent third-party empirical or measurement-validity certification.

## Release decision and remaining validation

- **PASS:** Exact-source Windows execution, all 37 unit tests and archived 600-scope/5,000-pair synthetic baseline reproduction.
- **PASS:** Provisional model-input decomposition and conservative incomplete-evidence handling within the implemented assumptions.
- **PASS for scope:** No governing equation, prior Lean theorem source, main model calibration file or accepted 41-page manuscript PDF was modified by this research-only increment.
- **OPEN:** Independent evidence verification, expert panel approval of 15 proxies, denominator and time-cap calibration, duplicate-source governance, prospective organization-specific measurement collection, blinded outcome adjudication and holdout baseline utility.
- **OPEN:** Actual empirical validation; no consented organization dataset or observed security outcome has been used.

**Merge recommendation:** The methodological pilot may be merged as a **clearly labeled provisional research addition** after the owner-local source test record and limitations are preserved. Do not label the CRPI scoring instrument field-validated, calibrated, predictive or suitable for automatic high-stakes decisions. Use [the prospective study protocol](../docs/EMPIRICAL_VALIDATION_STUDY_PROTOCOL.md) as the canonical next research gate. A new journal/manuscript revision is a separate editorial decision; this increment intentionally does **not** rebuild the 41-page published PDF.
