# CRPI v0.2 pre-submission review — exact-source acceptance and unresolved gates

**Assessment date:** 2026-10-28  
**Source under test:** `e24aa34f53223d3d27c0dab30d4b694107e10a20` (current manuscript and CI gate)  
**Push Actions run:** [40722583278](https://github.com/jmsbooth/cyber-risk-posture-model/actions/runs/40722583278)  
**PDF build promotion:** `2012b4a23d44831ba017bc2976bb58fc6ce2e9e7` (PDF-only bot commit)  
**Scope:** exact-source pre-submission *review* candidate, **not** independently peer-reviewed or empirically validated.

## Executed checks

| Gate | Evidence and disposition |
| --- | --- |
| Python regression | **PASS: 52/52** unit tests at source `e24aa34f`, including canonical SOE migration/legacy parity and the 44-field independent Decimal oracle |
| Stress and pilot archive parity | **PASS**: historical synthetic archives reproduce numerically when old v0.1 identifier spelling is translated in memory; original archives are unchanged |
| Preregistration safety | **PASS**: the hypothetical organizational pilot remains blocked with mandatory `--require-ready` exit 2 |
| Manuscript source | **PASS**: 30 cited and defined bibliography keys, no missing cross-references or duplicate labels; manuscript has no USOM identifier and uses a fixed review version |
| Lean build | **PASS**: renamed SOE mathematical source compiled with pinned toolchain and Mathlib in CI, including renamed mitigation and sensitivity lemmas |
| LaTeX build | **PASS**: full `latexmk` compilation, **49 pages**; release gate explicitly rejects overfull text, undefined references and missing characters |
| PDF structural checks | **PASS**: PDF rendered all 49 pages, no empty pages, no text outside physical page boundaries |
| Binary identity | SHA-256 `fcfbbc794bd538a89ad199f5ab7c2a24a8c9c36aa014b77c4873fad113ed8d22`; **430,996 bytes** from exact GitHub Actions artifact |
| Local visual review | Final-source PDF downloaded from CI artifact and inspected through five page-contact sheets; targeted higher-resolution inspection of title, primitive-input table, governing explanation, worked-example tables, three scientific figures, and closing/bibliography pages. Figures remain legible and line/color/marker encoding is distinct |

CI artifacts: [v0.2 Actions run](https://github.com/jmsbooth/cyber-risk-posture-model/actions/runs/40722583278), `crpi-v02-pdf-and-qa`.

## Formal proof-audit separation

The original 56-theorem evidence logs are tied to the pinned **pre-SOE** source revisions, and must not be relabeled. The renamed Lean sources passed fresh pinned builds and **all 56 theorem-level A/B/C `#print axioms` audits**, including after the final SOE notation correction. Source `480a8e3b13a428cd80beab69cb86d9e667e30875` passed in [GitHub Actions run 40723917611](https://github.com/jmsbooth/cyber-risk-posture-model/actions/runs/40723917611). The three uploaded audit logs contain **11 Phase A, 24 Phase B, and 21 Phase C** declaration results. An independent inspection of the archived log files confirmed that each listed only `propext`, `Classical.choice`, and `Quot.sound`; no additional axioms occurred. The standard proof assumptions and the original claim boundaries remain unchanged.

## Still open before release

- This is a **pre-submission review draft**, not an author-approved final preprint. The author must review the revised narrative and figures.
- The 30 reference entries have all internal keys resolved, but **source-by-source bibliographic and claim-level validation is unfinished**. See [bibliography audit](BIBLIOGRAPHY_AUDIT_V02.md).
- Obtain truly independent subject-matter review of construct semantics, novelty, persistence-rate identifiability, scope/inventory completeness, and the choice of max-envelope and regularized geometric aggregation.
- Confirm author identity/affiliation, disclosure and licensing policy, venue format, and submission consent.
- No organization has authorized intake under [Issue #9](https://github.com/jmsbooth/cyber-risk-posture-model/issues/9); no real evidence, independently adjudicated outcomes, empirically calibrated coefficients, or validated operational thresholds exist.
- On a final author-approved commit, regenerate the PDF and verify the **new exact SHA**. The hash above is an immutable receipt for this particular successful artifact, not for any later rebuild.

This QA does not certify outcome-validity, probability calibration, inferential power, or peer-review acceptance.

## Latest SOE symbol-level correction

A final notation audit identified two residual `\\widetilde{U}` primitive-variable occurrences in the SOE aggregation equation. Both were replaced by `\\widetilde{SOE}` and added as a fail-closed source check at source commit `480a8e3b13a428cd80beab69cb86d9e667e30875`. Full Python, Lean build/axiom audit, LaTeX, and PDF structural checks all **passed** in [run 40723917611](https://github.com/jmsbooth/cyber-risk-posture-model/actions/runs/40723917611).

The rebuilt exact-source **49-page** PDF was archived with SHA-256 `58c2da9ece68b4be5ae7a104cf2191cd34bb5aaa12e1023113e95f10f9881233` (434,280 bytes), promoted in PDF-only commit `4a9e5433630512295a26977f18a484263f240e94`, and visually inspected on representative pages including the SOE equation. The previous digest in this receipt remains historical for its corresponding pre-correction manuscript source. **The new PDF supersedes that earlier candidate.**
