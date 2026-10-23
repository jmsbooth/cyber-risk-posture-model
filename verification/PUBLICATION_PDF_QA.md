# CRPI Manuscript PDF — Publication QA Record

**Review date:** 2026-10-22  
**Issue:** [#5 — PDF publication closeout](https://github.com/jmsbooth/cyber-risk-posture-model/issues/5)  
**Artifact under review:** Owner-uploaded Tectonic 0.17.0 PDF generated from local `main` at `971e3684a511e9d92a7e2e311a27ad5567c80bce`.  
**Original PDF SHA-256:** `242e0276874e063bee1bf8dcc69cd25a22712b801fc7af926ff27290ca20b7d9`  
**Original PDF size:** 224,553 bytes (39 US Letter pages).  
**Status: FINAL PUBLICATION PDF ACCEPTED — source-matched, clean Tectonic build, and 39/39 rendered-page visual QA passed.**

**Revision boundary (2026-10-23):** This QA approval belongs **only** to the previously published PDF with SHA-256 `2897fe42fb4639851f703389ce575c96bec622a2d0b102cd6f803364319bcb2c` (225,519 bytes; 39 pages) and its PR #6 LaTeX source. Research PR #7 now contains a different **236,974-byte** PDF, SHA-256 `b7ff8043aa2f043b371c48f98520c45cf776c2f797ea7271455eccac507afe54`, with added operational-input and synthetic-stress sections. Its source compile and binary checksum are accepted, but **this historical 39-page render signoff cannot be transferred to the revised artifact**. The new PDF's page-by-page rendered inspection is pending; see [PR #7 stress/rebuild acceptance](STRESS_WINDOWS_REPLAY.md).

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
- The owner also received an ignored-parent-directory error when adding `paper/build/CRM_revised.pdf`. This can arise if a user/global `build/` exclusion matches the directory before the repository's negated PDF filename rule can apply. The repository `.gitignore` now explicitly unignores **both** `paper/build/` and `paper/build/CRM_revised.pdf`; the owner ultimately needed `git add -f -- paper/build/CRM_revised.pdf` on this workstation because the normal add still considered the parent directory ignored; only the intended binary was staged. The precise source of the owner's ignore rule can be checked with `git check-ignore -v paper/build/CRM_revised.pdf`.

**Independent targeted test (not full-manuscript acceptance):** A native XeLaTeX document exercising the exact abstract, representative four-column table, and the two affected proof/model-risk paragraphs compiled without `Overfull` warnings; table text remained inside the normal text margins and was visually checked. This isolated test cannot substitute for a full Tectonic build or inspection of the regenerated final PDF.

**Resolution:** A later full-manuscript Tectonic 0.17.0 build passed with zero `Overfull`, `Undefined` and `Missing character` log matches. The earlier `b85f...` artifact remains rejected. See the final-artifact record below. The draft PR remains unmerged pending exact-binary page-by-page visual review.

## Corrected artifact committed to PR #6 — technical acceptance

On 2026-10-22 the repository owner rebuilt the publication branch at source revision `bb39680884a44503b4371aa9ccd140a26ba65a42` using **Tectonic 0.17.0**. The engine completed TeX, reran cross-references, and wrote the PDF with exit code zero. A search of the full retained `CRM_revised.log` returned **zero occurrences** of `Overfull`, `Undefined`, and `Missing character`. A nonfatal Fontconfig default-configuration message appeared in stderr; the build was successful.

| Artifact property | Result |
| --- | --- |
| Path | `paper/build/CRM_revised.pdf` |
| Build source revision | `bb39680884a44503b4371aa9ccd140a26ba65a42` (no LaTeX edits subsequently) |
| Binary committed to branch | `dd74d58` |
| Size | **225,519 bytes** |
| SHA-256 | **`2897fe42fb4639851f703389ce575c96bec622a2d0b102cd6f803364319bcb2c`** |
| GitHub blob SHA-1 | `24747ec6aca8c21d64505db2c51dfcb9810b8620` |
| PDF header | `%PDF-1.5` |
| TeX overfull/undefined/missing-character diagnostics | **0 matching log entries** |
| [Tracked GitHub PDF](../paper/build/CRM_revised.pdf) | **Present on publication branch**, hash independently recomputed from GitHub's exact base64 file bytes |
| Direct README download link | **Added on the publication branch** |
| Exact-binary full-page visual/geometry inspection | **PASS**, all 39 pages rendered and reviewed, plus targeted high-resolution inspection of corrected equation/table pages |
| Final PDF properties | **39 US Letter pages**, 30 numbered bibliography entries, four plotted figures, six appendix propositions, 70 link annotations; all fonts embedded, no replacement glyphs or unresolved `??` tokens; PDF/UA tagging absent (not required for this release) |

**Binary provenance check:** The GitHub connector returned the entire committed PDF as base64. Independent SHA-256 computation over those decoded bytes exactly matched the Windows `Get-FileHash` result, and byte count matched the git commit. Therefore no local rebuild/re-upload is required unless the page-render review identifies a substantive defect. The earlier visual results for the pre-correction PDF are historical evidence, not verification of the corrected binary's pagination.

**Final gate decision:** ACCEPTED. The corrected tracked binary passed all 39-page visual QA and technical preflight. PR #6 may be marked ready, merged into `main`, and Issue #5 closed after the direct tracked PDF link on `main` resolves.

## Final exact-file render-based review — PASS

The user attached the final `CRM_revised(1).pdf`; its SHA-256 matched the **GitHub-tracked** PDF exactly: `2897fe42fb4639851f703389ce575c96bec622a2d0b102cd6f803364319bcb2c`. The uploaded file was processed with PyMuPDF/Poppler from its actual bytes, **not** the original 39-page artifact or a filename-based inference.

- **39/39 pages** rasterized and inspected using ten 2×2 page montages, plus enlarged page images for the original defect sites (especially PDF pages **8–9, 25–26 and 31**) and graphics/appendix sections. Every page contains readable content, including a short concluding reference page 39; no missing/blank pages.
- Text-span geometry check on **all 39 pages**: no text bounding boxes beyond PDF page edges and **no text exceeding the normal 72–540 pt horizontal margins**. Equation **(21)** on page **9** remains intact and safely within margins; the earlier overhang is gone. The former overflow near the page **8** worked example is gone, with a minor line break within the inline `CRPI(t+1)` expression remaining legible (nonblocking typographic imperfection).
- Tables **10** (page 25), **11** (page 26), and **13** (page 31) have readable ragged-right columns, consistent numerical alignment and no visible column collisions or clipping. Five additional corrected measurement tables also fit the text width.
- Figures **1–4** (pages 18, 28 and 29) show visible chart data, axes, legends and captions. Figures use vector graphics rather than embedded bitmap images.
- 30 numbered bibliography entries, Appendix Propositions **1–6**, 70 internal/external link annotations, all listed fonts embedded, no U+FFFD replacement characters, no unresolved `??` tokens, no PDF encryption, no blank pages. The PDF remains **untagged for PDF/UA**; tagging was not a requirement of this paper's publication milestone.
- The Tectonic 0.17.0 log **independently supplied by the owner** reported compilation exit zero and **zero** `Overfull`, `Undefined`, or `Missing character` diagnostics. Nonfatal Windows Fontconfig default-configuration noise had no observable impact on the final rendered PDF.
- **Visual QA outcome:** all material originally identified publication defects are resolved. No further TeX edits or rebuild are required for this milestone. Mathematical model correctness and empirical calibration remain separate from visual publication quality.

## Corrections prepared in this PR

- Layout-only edits to `paper/CRM_revised.tex`, including the two overlong displays and three dense tables.
- `.gitignore` revised so only `paper/build/CRM_revised.pdf` can be tracked within the TeX build directory; logs and auxiliary files remain ignored.
- Targeted independent XeLaTeX layout probes of the table formatting passed compilation and rendered readable Tables 10, 11 and 13. A first probe exposed an unbreakable inline analytical-level list, which was corrected in source before opening this PR.

**Final decision:** The corrected, source-matched PDF has now passed independent rendered-page review, not just isolated test compilations. The earlier original and first revised artifacts remain rejected. All final acceptance criteria below are satisfied in the bounded publication scope; this does not assert empirical validation.

## Final acceptance checklist

1. **PASS:** Full Tectonic 0.17.0 PDF build on source revision `bb39680884a44503b4371aa9ccd140a26ba65a42`, zero publication-impacting LaTeX diagnostics.
2. **PASS:** Final exact binary size 225,519 bytes and SHA-256 `2897fe42fb4639851f703389ce575c96bec622a2d0b102cd6f803364319bcb2c`, independently matched to the committed GitHub bytes from `dd74d58`.
3. **PASS:** 39/39 rendered-page visual and layout inspection, source-matched and margin-checked, with corrected figures, tables, appendix and bibliography.
4. **PASS:** Published tracked artifact at `paper/build/CRM_revised.pdf` and README-relative direct PDF link in this PR.
5. **RELEASE DECISION:** Ready to merge PR #6 with retained file/content provenance. Verify the README link on `main` after merge, and close Issue #5. No empirical validation or all-purpose model proof is implied.

**Out of scope:** Re-running previous source-matched Lean/Python mathematical verification solely for typographic edits; empirical calibration; creating a scientific-release tag. The underlying governing equations, their labels, table numeric values, and the 56 previously accepted Lean theorem statements are unchanged.
