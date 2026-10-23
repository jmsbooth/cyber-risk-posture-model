# CRPI Operational Stress Test — Windows Replay Acceptance

**Date:** 2026-10-23  
**Repository:** `jmsbooth/cyber-risk-posture-model`  
**PR:** [#7 — Minimum operational inputs and synthetic failure-mode analysis](https://github.com/jmsbooth/cyber-risk-posture-model/pull/7)  
**Result:** **PASS — numerical/reproducibility acceptance and independently completed revised-PDF visual publication QA**.

## Owner-local acceptance evidence

The repository owner reported the following PowerShell commands executed from a Windows checkout of source revision **`2d09081649ecee89fc6db749d66c2d897cb0b3fe`**.

| Check | Owner-reported result |
| --- | --- |
| `git pull --ff-only origin research/crpi-operational-inputs-and-stress-tests` | Fast-forward to `2d09081` |
| `python scripts/run_stress_tests.py --check verification/stress_test_results.json` | **`Reproducibility PASS`**; exact stored 12,000-draw result replay |
| `python -m unittest discover -v` | **`Ran 25 tests in 6.390s`**, **`OK`**; all old and new tests passed |
| `test_archived_evidence_reproduces` | PASS |
| `test_calibration_hash_is_independent_of_checkout_line_endings` | PASS |
| `test_partial_interval_covers_truth` | PASS |
| `test_time_order_noncommutes_but_static_semigroup_holds` | PASS |
| Independent Phase D Decimal reference oracle | Reported **44 fields verified** within the existing test suite |

The output reproduces `verification/stress_test_results.json` without updating the archived results. The run was performed directly against `models.crm_reference` imported by the committed stress runner—not solely against the earlier isolated equation-equivalent harness. It resolves the earlier Windows CRLF-vs-LF metadata mismatch.

**Evidence scope:** These are results from the repository owner's console output, transcribed here as a review record. They are not automatically captured signed test logs or CI attestations. The exact 12,000-draw JSON and method/script are committed and inspectable; the output proves reproducibility on the reported local runtime but does not establish statistical validity for real organizations.

## Selected reproduced results (synthetic only)

- Base draw count **12,000**, zero score-boundedness violations, median instantaneous residual **0.119813353**.
- 10% random missingness: median residual possible-value bound width **0.048736848**, **37.0%** of synthetic intervals cross an *illustrative* 0.15 threshold.
- 20% random missingness: median bound width **0.138673033**, **63.95%** of synthetic intervals cross 0.15.
- Risk-correlated omitted measurements: observed fraction **0.931438889**, neutral-fill mean signed residual bias **−0.009016511**, and **0.210376135** of *above-cutoff synthetic cases* missed by neutral fill.
- Consequence-weight change reversed **0.104833333** of **6,000** pairwise rankings.
- Two exposure/mitigation sequences with identical weekly means ended at persistent stocks **0.030237968** and **0.37940925**, while a coarse weekly-mean update yielded **0.138302755**. Fixed-input semigroup difference was reported as **0.0**.

The comparison cutoff is entirely uncalibrated. These are diagnostics of equation semantics under invented sampling and missingness mechanisms, not field-estimated incident rates, risk probabilities, or decision thresholds.

## Post-run source integrity

After the reported exact-revision test run, commit **`c6b4d39673a9e9f9aeaae1c83c87f3c8a944831b`** added **only** the rebuilt manuscript binary `paper/build/CRM_revised.pdf`. GitHub comparison `2d09081...` to `c6b4d39...` confirmed no changes to scripts, tests, data dictionary, calibration JSON, result JSON, source manuscript TeX, or Lean proof files.

The owner also built `paper/CRM_revised.tex` with **Tectonic 0.17.0**, and searched the retained log for `Overfull`, `Undefined`, and `Missing character`. The search returned no matches. The revised PDF was tracked and committed in `c6b4d39` (236,974 bytes). Its exact SHA-256 was **independently recomputed from the GitHub binary**:

`b7ff8043aa2f043b371c48f98520c45cf776c2f797ea7271455eccac507afe54`.

**Separate revised-PDF visual QA accepted (2026-10-23):** The user uploaded the exact revised 236,974-byte binary, and its SHA-256 again matched GitHub and the Windows build. All **41/41 pages** were rasterized and inspected, including high-resolution review of the new Sections 8.4 and 11.3 (PDF pages 25, 32–33), mathematical appendix, Figures 1–4 and end matter. No text left nominal 72–540pt horizontal margins, no blank pages or missing images were found, and all listed fonts are embedded. The complete [current-revision publication QA record](PUBLICATION_PDF_QA_PR7.md) documents the checks, distinct from the old 39-page approval.

## Mathematical interpretation and release gate

The core CRPI equations and previously verified 56 conditional Lean declarations are unchanged. The operational input dictionary remains **provisional**, with uncalibrated raw-telemetry-to-score normalization and other explicitly documented organizational-data limits. Stress percentages and a selected threshold are synthetic and carry no empirical predictive-performance claim.

**Decision:** Stress-test source/archived-results acceptance **PASS** (all **25/25 tests**). PDF compilation, SHA-256 byte provenance and **41-page visual QA PASS**. PR #7 is publication-merge eligible within these documented mathematical and synthetic-research bounds. No empirical risk-model validation is implied.
