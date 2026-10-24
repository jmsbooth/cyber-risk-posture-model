# CRPI measurement pilot and structural baseline comparison — initial technical evidence

**Status:** Experimental source-backed *methodology only*. **No real organizational evidence was ingested, no observed incident outcomes were used, and no CRPI calibration was established.** The model and previously accepted mathematical theorem files remain unchanged.

**Date:** 2026-10-23  
**Source:** [`models/operational_pilot.py`](../models/operational_pilot.py) + [provisional pilot measurement profile](../config/measurement_pilot_v0.1.json)  
**Evidence:** [`measurement_pilot_structural_results.json`](measurement_pilot_structural_results.json), [fictional normalized assessment](operational_pilot_example.json), [test suite](../tests/test_operational_pilot.py)

## Executed local methodology check

The implementation was exercised with Python **3.13.5** in an isolated container mirroring the relevant six core CRPI functions from `models.crm_reference`. The cloned functions implement the original formulas; because this workspace has no DNS access to GitHub, this is **not yet a test against the exact checked-out full repository module**. The 12 new pilot tests passed, including comparison of the raw-evidence adapter's instantaneous residual with the existing stress-runner's score for the same 15 normalized primitives. The owner has now executed the complete checked-out repository suite on Windows: **37/37 unit tests passed** and the archived structural comparison returned **`Pilot structural reproduction PASS`**. The initial isolated 12-test execution remains a separate historical development record. See [the exact-checkout acceptance and semantic review](MEASUREMENT_PILOT_WINDOWS_ACCEPTANCE.md). Reproduction files are versioned; their contents are **synthetic**.

## Fictional assessment and normalization stress

The input fixture is a single **fictional** business service with all 15 pilot raw observations assumed to be contemporaneous and asserted verified (the assertions are not independently authenticated). It carries a fictional prior stock of `0.4` and `dt=1` day. The full input decomposition returns:

| Scenario | Model output |
| --- | ---: |
| Raw evidence baseline, instantaneous residual `R_inst` | **0.039969698** |
| Raw evidence baseline, temporal envelope `CRPI` | **0.239723943** |
| Pilot governing-path evidence completeness | **1.0** (fictional assertions only) |
| Unchanged exposed-asset numerator but smaller denominator (5/20 -> 5/10): residual | **0.057313503** |
| Same altered denominator: CRPI | **0.242496513** |
| Same observed response time, but time cap `U=72h` -> `U=24h`: residual | **0.053370091** |
| Same altered time cap: CRPI | **0.263346481** |
| Missing `TE_external`: possible residual interval | **[0.011190487, 0.082672143]** |
| Missing `TE_external`: reportable point CRPI | **null** |
| Stale `USOM_detection`: reportable point CRPI | **null** |

These differences demonstrate **denominator dependence**, **normalizer/profile sensitivity**, and **state masking**. None quantifies the accuracy of the measurements or predicts incidents. The completeness value `1.0` reflects fixture declarations, not confidence that a real organization is comprehensively measured. The risk interval covers only variation of an unknown normalized primitive with all other profile values held fixed, **not** measurement/model uncertainty or a confidence interval.

## Structural comparators — fixed seed 20261023

The baseline script sampled **600 independent synthetic one-interval scopes** from 15 independent `Beta(2,2)` normalized primitives and independently invented `Beta(2,2)` prior stocks. It compared **5,000 randomly selected pairs**, using the same rows/profile. This design is a deliberate stress case for ranking, not a field sample and not a statistical power study.

| Score | Mean of synthetic scores | Rank reversal vs CRPI | Interpretation |
| --- | ---: | ---: | --- |
| CRPI envelope | 0.411039452 | reference | Stock-aware model index |
| Stateless instantaneous residual | 0.128964492 | **44.70%** | Removing inherited stock changes rank order substantially under deliberately independent prior stocks |
| Simple adverse additive `(TE + D_eff + 1 - M)/3` | 0.517764267 | **43.92%** | A different, non-mechanistic construct; absolute score is **not** comparable to CRPI |
| Arithmetic TE ablation, otherwise same CRPI model | 0.412225984 | **0.28%** | Replacing only geometric TE aggregation with arithmetic TE had a small effect under *this* synthetic sampling/profile |

The large stateless/additive rank differences partly follow from the **synthetically independent stock**. They cannot be interpreted as evidence that CRPI has better predictive validity, superior security semantics, or calibrated absolute scores. No outcomes were generated or imported, so no ROC AUC, model skill, causal effect, Brier score or significance test would be justified.

## Open validation and acceptance gate

- [x] Fifteen raw-proxy fields mapped to normalized scores without changing canonical equations.
- [x] Fractions require nonzero, positive denominators; ordinal and elapsed-time inputs enforce governed type/range.
- [x] Source/time-zone/freshness/reviewer assertions and time-sample eligibility are assessed per evidence record.
- [x] Missing/stale/unverified/undersampled evidence returns no point CRPI and a bounded feasible residual interval.
- [x] Temporal cold start explicitly labeled rather than inferred; `S` and active output branch retained in decomposition.
- [x] Synthetic pilot data, normalizer/denominator stress and three structural baselines are executable and repeatable locally.
- [x] Twelve targeted local pilot tests passed (Python 3.13.5, isolated source-faithful core functions).
- [x] **Run the full repository suite on the owner's Windows source checkout**: `Ran 37 tests in 6.041s — OK`; the Phase D Decimal oracle verified 44 expected fields; the deterministic 600-scope structural results replayed. The console evidence and source/test boundary are recorded in [MEASUREMENT_PILOT_WINDOWS_ACCEPTANCE.md](MEASUREMENT_PILOT_WINDOWS_ACCEPTANCE.md). This is manual developer evidence, not CI or a signed external audit.
- [x] Scope-limited **internal semantic review** of proxy-to-construct mappings, denominator gaming, duplicate evidence, time-cap selection and ordinal assumptions; concrete open validity risks are recorded in [MEASUREMENT_PILOT_WINDOWS_ACCEPTANCE.md](MEASUREMENT_PILOT_WINDOWS_ACCEPTANCE.md). **Independent external/domain-expert review remains open** before real organizational measurement or calibration claims.
- [ ] Ingest consenting organizational evidence, predeclare measurement definitions/observed outcomes, assess reviewer agreement, calibrate on training data and assess holdout utility. This is the actual *empirical validation* phase.

**Decision:** Exact-source Windows execution and reproducible synthetic research acceptance **PASS**. The operational measurement pilot is eligible to merge **as provisional methodology only**. Organizational measurement validity, proxy calibration, expert-reviewed evidence definitions and prospective holdout utility remain unestablished; no regulatory, validated-threshold, probability or model-superiority claim is supported by these results.