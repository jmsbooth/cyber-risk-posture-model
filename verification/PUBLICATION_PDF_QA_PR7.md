# CRPI — Operational Input and Synthetic Stress Revision PDF QA

**Date:** 2026-10-23  
**Subject:** [PR #7 — Operational input contract and synthetic failure-mode analysis](https://github.com/jmsbooth/cyber-risk-posture-model/pull/7)  
**Scope:** The **new** manuscript PDF containing Sections 8.4 and 11.3; this is distinct from the separately approved October 22 39-page release.  
**Disposition: ACCEPTED FOR PUBLICATION — exact-binary 41-page rendered QA passed.**

## Source, compilation and binary identity

- Tested mathematical/stress Python source revision: `2d09081649ecee89fc6db749d66c2d897cb0b3fe`.
- Windows owner-reported `python scripts/run_stress_tests.py --check verification/stress_test_results.json`: **Reproducibility PASS**, exact archived 12,000-draw JSON.
- Windows owner-reported `python -m unittest discover -v`: **25/25 passed** (including LF/CRLF normalization regression and the Phase D 44-field Decimal oracle).
- Tectonic 0.17.0 full-manuscript compilation: **PASS**. Search of the source build log for `Overfull`, `Undefined`, and `Missing character`: **zero matches**. These compiler results are owner-provided console evidence.
- The revised PDF was added in commit `c6b4d39673a9e9f9aeaae1c83c87f3c8a944831b`. GitHub compare from the tested revision to that commit showed **only the PDF binary changed**. Subsequent branch commits update documentation and acceptance records, not equations, tests, vectors, calibration data or LaTeX.
- **Artifact:** `paper/build/CRM_revised.pdf`; **236,974 bytes**; PDF 1.5, 41 US-Letter pages, not encrypted.
- **SHA-256:** `b7ff8043aa2f043b371c48f98520c45cf776c2f797ea7271455eccac507afe54`; verified three ways: owner Windows `Get-FileHash`, independently recomputed from the **complete GitHub binary** (Git blob SHA-1 `4d3c6d84179e55c1a69205d8f47a76105e251e08`), and the **actual PDF uploaded to the conversation**. All three values match exactly.

## Full revised-PDF visual and structural review

The exact 236,974-byte PDF was mounted locally and opened with PyMuPDF. All **41 pages** were rasterized, reviewed across 11 page-contact sheets (110% scale), and high-resolution inspected at the new research sections, mathematical and tabular material and end matter (including pages **8–9, 25–27, 29–30, 31–34, 37–41**).

| Acceptance criterion | Observed result |
| --- | --- |
| PDF completeness / rendering | **PASS**, all 41 pages rasterize; every page has extractable content; no blank or malformed pages |
| Horizontal body margin | **PASS**, no text spans outside **70–542 pt** tolerance; inspected spans lie on/inside nominal 72–540 pt margins |
| Physical page boundaries | **PASS**, no text beyond page edges |
| New Section 8.4 — Minimum Operational Inputs | **PASS**, page 25; eight/nine governed-input distinction, 15 primitive decomposition, missing-input policy and referenced artifact names legible |
| New Section 11.3 — Executed Synthetic Stress Experiments | **PASS**, pages 32–33; intact 12,000-draw methodology, 10%/20%/risk-correlated missingness, weight-rank and temporal-order findings |
| New stress Table 13 | **PASS**, page 32; aligned and readable multi-line headings; data `0.0487`, `0.1387`, `0.0289`; `37.0%`, `64.0%`, `29.7%`; `10.8%`, `18.5%`, `21.0%` agree with stored synthetic results after rounding |
| Sensitivity Table 14 | **PASS**, page 33; no cross-column collision; all numeric columns and scenario descriptions visible |
| Governing equations and Proposition 1–6 | **PASS**, equations legible and within page margins; all six mathematical propositions present on pages 37–38 |
| Figures 1–4 | **PASS**, vector graphics and captions readable on pages 18, 29 and 30; no missing axes, graphics or legends |
| Measurement, calibration and summary tables | **PASS**, Tables 1–14 present, continued longtable headers readable, no clipping or column overlap detected |
| Bibliography | **PASS**, 30 numbered references through page 41; no empty trailing pages |
| Fonts and text encoding | **PASS**, listed fonts embedded; selectable/extractable text; no detected U+FFFD replacement glyphs, no `??` unresolved cross-reference tokens |
| PDF links | **71** document link destinations enumerated with PyMuPDF |
| PDF accessibility | PDF is not PDF/UA tagged; tagging was not included in the manuscript's agreed publication gate |

**Minor nonblocking layout notes:** A few inline file paths in the new sections wrap across lines, but remain unambiguous and readable; longtable continuations are correctly labeled; the final bibliography occupies part of page 41 without an unintended blank page. None of these warrants rebuilding the accepted source.

## Scientific scope and release decision

- The calculations are simulations of a specified model with **invented Beta(2,2) input distributions** and governed illustrative calibration, not field observations. The 0.15 split used to examine missed classifications is an *illustrative decision boundary*, not an operational threshold.
- The selected worst-case missing-input intervals are **possible-value ranges**, not probabilistic confidence intervals. Profile-sensitive rankings and cadence aliasing limit naive cross-organization and aggregated-time comparisons.
- The **56 previously accepted conditional Lean theorem declarations**, bounded numerical conformance and 25 Python tests do not establish empirical calibration, breach probability or predictive model validity.
- The provisional 15-input dictionary still needs organization-specific raw-evidence normalization, measurement owners and calibration to function as a turnkey field assessment.

**Final acceptance:** The new research PDF is **publication-quality within the established PDF technical/visual gate**, and the numerical archive is independently reproducible on the owner workstation. PR #7 is cleared to become ready and merge to `main` without another PDF build or new tests. Update README to refer to this **41-page**, newly accepted file (not the old 39-page QA), then verify the direct link and GitHub binary on `main` after merge. Preserve the older [PDF QA record](PUBLICATION_PDF_QA.md) as historical, binary-specific evidence.
