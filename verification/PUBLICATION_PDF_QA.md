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

## First revised full-manuscript build — remaining warnings

On 2026-10-22, the owner built the first typographically revised branch with **Tectonic 0.17.0**. The engine exited successfully, producing PDF SHA-256 `b85f658119abfacb18ac3a47a6e4403b9e9d0ce17896e0709a30005db0175cc9` and writing `paper/build/CRM_revised.log`. This first post-correction build was **not accepted**: with `\\hfuzz=2pt` restored, the log exposed 18 overfull boxes per TeX pass (the messages were repeated on the second compilation pass).

- Fifteen identical **10.4187pt** overfull alignment warnings came from the header and repeated headers of five four-column submetric measurement `longtable` environments: source lines 639–657, 703–720, 774–791, 991–1010 and 1074–1091. The five tables used column fractions summing to `0.92\\textwidth`, which **plus eight default tabcolsep paddings** exceeded the text block width. The column fractions now sum to **0.88\\textwidth** with ragged-right `P{}` cells.
- Three paragraph warnings occurred at source lines 40–55 (**16.74695pt**, abstract), 1685–1695 (**3.25648pt**, model risk) and 1840–1842 (**5.739pt**, directional sensitivity proposition). A restrained `\\emergencystretch=2em` was added to allow less severe line-spacing/break adjustments without suppressing margin diagnostics.
- The owner also received an ignored-parent-directory error when adding `paper/build/CRM_revised.pdf`. This can arise if a user/global `build/` exclusion matches the directory before the repository's negated PDF filename rule can apply. The repository `.gitignore` now explicitly unignores **both** `paper/build/` and `paper/build/CRM_revised.pdf`; the workaround `git add -f` is not needed when the updated rules are effective. The precise source of the owner's ignore rule can be checked with `git check-ignore -v paper/build/CRM_revised.pdf`.

**Independent targeted test (not full-manuscript acceptance):** A native XeLaTeX document exercising the exact abstract, representative four-column table, and the two affected proof/model-risk paragraphs compiled without `Overfull` warnings; table text remained inside the normal text margins and was visually checked. This isolated test cannot substitute for a full Tectonic build or inspection of the regenerated final PDF.

**Current action:** Rebuild from the latest publication branch and inspect the new log. The earlier `b85f...` PDF **must not** be committed as final; source now has further changes. The draft PR remains unmerged pending a warning-free full build and page-by-page PDF inspection.

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
