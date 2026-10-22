# CRPI Manuscript PDF — Publication QA Record

**Review date:** 2026-10-22  
**Issue:** [#5 — PDF publication closeout](https://github.com/jmsbooth/cyber-risk-posture-model/issues/5)  
**Artifact under review:** Owner-uploaded Tectonic 0.17.0 PDF generated from local `main` at `971e3684a511e9d92a7e2e311a27ad5567c80bce`.  
**Original PDF SHA-256:** `242e0276874e063bee1bf8dcc69cd25a22712b801fc7af926ff27290ca20b7d9`  
**Original PDF size:** 224,553 bytes (39 US Letter pages).  
**Status: PDF COMPILATION PASS; ORIGINAL VISUAL QA NOT APPROVED; TYPOGRAPHIC REMEDIATION STAGED; REBUILD AND RE-INSPECTION REQUIRED.**

## Original PDF checks completed

The exact uploaded binary matches the owner's reported SHA-256. PDFium/Poppler rendered every page without errors. Pages 1–39 were reviewed by montage, with pages 8, 9, 25, 26, 31, and 36 individually inspected at higher resolution. All referenced fonts are embedded, the PDF has extractable/selectable text, and no page is blank. Text extraction found 30 bibliography entries, six appendix propositions, and no `??` unresolved-reference tokens or replacement glyphs. The extracted PDF contains 70 link annotations.

Figures 1–4 (PDF pages 18, 28 and 29) rendered with axes and captions. The title, author and date appeared on page 1; page numbering ran through 39. The manuscript explicitly distinguishes an operational posture index from breach probability/financial loss and does not claim empirical validation.

### Publication findings in the uploaded binary

| Priority | Page in uploaded PDF | Finding | Proposed source remediation |
| --- | --- | --- | --- |
| **P0** | 9 | Scoped CRPI Equation (21) had an unbroken set of analytical levels extending to approximately x=603pt on a 612pt page; normal right margin ends near x=540pt. While not cut off by page edge, it is publication-grade margin overflow. | Keep the identical `CRPI_{u,\ell}(t)=\max(R_{\mathrm{inst},u,\ell}(t),S_{u,\ell}(t))` equation, state the valid analytical levels in breakable prose. The `eq:scoped-crpi` label remains unchanged. |
| **P1** | 8 | Worked-example inline envelope arithmetic extended into right margin by approximately 28pt. | Present the already computed `CRPI(t+1)=0.182` in shorter prose without changing the calculation. |
| **P1** | 25 | Table 10 combined five narrow, fully justified columns; unnatural whitespace, broken words, and apparent cross-column collisions impaired readability. A duplicated `\begingroup` and `\tabcolsep` setting complicated layout. | Use the existing `P{}` ragged-right column type, redistribute widths, improve row spacing, remove duplicate group. |
| **P1** | 26 | Table 11's fully justified narrow columns created large interword gaps and over-compressed interpretation text. | Use three ragged-right `P{}` columns with calibrated width and padding. |
| **P1** | 31 | Table 13 used an unnecessarily narrow scenario column, splitting labels into many short lines. | Expand scenario width, use ragged-right text, maintain numeric columns and exact values. |
| **P2** | 37 | One supplementary-input bullet exceeded the normal right margin slightly. | Re-punctuate the identical TE submetric enumeration for normal line breaks. |
| **Build hygiene** | Source preamble | `\hfuzz=1000pt` suppressed diagnostic reporting of severely overfull horizontal boxes. | Set `\hfuzz=2pt` so future Tectonic builds report overflows rather than silently ignoring them. |

No page text block was outside the physical PDF page boundaries; the findings concern **normal body-text margins and readability**, not file corruption. The PDF is not tagged for PDF/UA accessibility; tagging remains an optional future publishing improvement, not a silent pass claim.

## Corrections prepared in this PR

- Layout-only edits to `paper/CRM_revised.tex`, including the two overlong displays and three dense tables.
- `.gitignore` revised so only `paper/build/CRM_revised.pdf` can be tracked within the TeX build directory; logs and auxiliary files remain ignored.
- Targeted independent XeLaTeX layout probes of the table formatting passed compilation and rendered readable Tables 10, 11 and 13. A first probe exposed an unbreakable inline analytical-level list, which was corrected in source before opening this PR.

**Critical distinction:** Targeted isolated layout probes do **not** establish that the full revised 39-page manuscript has passed Tectonic or the complete page-by-page visual QA. The uploaded, pre-correction PDF is **not** the releasable artifact. This PR is **draft** until the rebuilt PDF is supplied and accepted.

## Required final acceptance

1. Rebuild `paper/CRM_revised.tex` with Tectonic 0.17.0 from the publication branch. Review log output for actual `Overfull\hbox`, undefined references, missing fonts, and build errors; do not suppress warnings without inspecting them.
2. Preserve exact commit SHA, source TeX SHA-256, PDF SHA-256, file length, Tectonic version, page count and build result.
3. Upload the rebuilt `CRM_revised.pdf` for complete 100%-page rendering. Confirm margin bounds on formerly problematic pages and check for any pagination-induced new defects.
4. Commit the accepted PDF to `paper/build/CRM_revised.pdf` on this PR. Confirm the binary SHA-256 matches the reviewed revision. Do not put earlier pre-correction artifact in `main`.
5. Update README to link directly to the tracked PDF, confirm the URL resolves, then merge this PR and close Issue #5.

**Out of scope:** Re-running previous source-matched Lean/Python mathematical verification solely for typographic edits; empirical calibration; creating a scientific-release tag. The underlying governing equations, their labels, table numeric values, and the 56 previously accepted Lean theorem statements are unchanged.
