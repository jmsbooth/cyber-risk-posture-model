# CRPI foundation paper — external review readiness assessment

**Assessed:** 2026-10-25  
**Repository baseline:** `main` @ `0ed3d9ef9ab52627068abeccebf100b58dc4e308`  
**Manuscript:** `paper/CRM_revised.tex`; accepted 41-page PDF `paper/build/CRM_revised.pdf`  
**Disposition:** **READY TO SOLICIT PRE-SUBMISSION SCIENTIFIC CRITIQUE**, with outstanding editorial and verification tasks; **NOT YET AUTHOR-APPROVED FOR PREPRINT OR JOURNAL SUBMISSION**. This is an internal readiness analysis, not independent referee acceptance.

## Reviewed evidence

- The manuscript explicitly describes CRPI as an **operational posture index**, not a breach probability, financial-loss estimate or security guarantee. It identifies the framework-agnostic five Tier-2 constructs, resilience-adjusted consequence, observability-modulated mitigation, bounded persistent stock and conservative envelope.
- The appendix states six propositions. [Proof coverage](../verification/PROOF_COVERAGE_MATRIX.md) records **56 source-matched conditional Lean theorem declarations** supporting selected mathematical subclaims; it excludes a machine-checked proof of the P6 switching-boundary nondifferentiability observation and any broad empirical-validity conclusion.
- [Phase D](../verification/PHASE_D_STATUS.md) and [reproducibility evidence](../verification/STRESS_WINDOWS_REPLAY.md) document numerical reference checks. The synthetic stress experiment uses 12,000 sampled input configurations with an illustrative profile; it is **not an organizational dataset**.
- [Publication QA for PR #7](../verification/PUBLICATION_PDF_QA_PR7.md) records Tectonic 0.17.0 compilation and visual QA of **41/41 pages**, 14 tables, four figures, 30 references, and SHA-256 `b7ff8043aa2f043b371c48f98520c45cf776c2f797ea7271455eccac507afe54`. This assessment relies on that documented historical QA; it does **not** independently download, render, or rebuild the PDF.
- Static source check of `paper/CRM_revised.tex` found **30/30 bibliography entries cited**, no missing/duplicate bibliography keys, **31 unique labels**, no missing `\\ref`/`\\eqref` targets. The source uses `\\date{\\today}`, which is not a stable version date.
- [PR #11](https://github.com/jmsbooth/cyber-risk-posture-model/pull/11) added organizational pilot-preparation documents only. [Issue #9](https://github.com/jmsbooth/cyber-risk-posture-model/issues/9) is **open**: 26 preregistration/governance gates remain, no partner is enrolled, no authorized empirical input or independently adjudicated outcome has been collected.

## Research and submission gates

| Priority | Gate | Assessment / acceptance criterion |
| --- | --- | --- |
| P0 | **Independent novelty assessment** | Referees compare the contribution directly against recent dynamic risk assessment, including Cheimonidis–Rantos (2025), DRIMAX (2026), attack-graph/Bayesian alternatives and operational risk indices. Document exact distinctions and remaining overlap rather than asserting uniqueness. |
| P0 | **Functional-form justification and falsifiability** | Challenge why regularized geometric aggregation, \(TE D_{eff}\), the CM × USOM mitigation term, stock-flow rates and the max-envelope are preferable for the stated constructs. Produce counterexamples and comparisons with simpler candidate forms; mathematical boundedness alone does not prove those are valid measurements. |
| P0 | **Claim and scope audit** | Keep formal proof, numerical conformance, synthetic sensitivity and prospective empirical validation clearly disjoint. Avoid any unsupported "validated cyber risk" claim, implied probability, field calibration or predictive superiority. |
| P1 | **Author and ethics/IP metadata** | Confirm author name, affiliation or independent-researcher status, contact, ORCID if available, conflicts, funding, acknowledgments, AI assistance as required, IP clearance and code/text license. Do not invent affiliation. |
| P1 | **Stable version identity** | Replace publication-facing `\\date{\\today}` with an author-approved date/version, and create a tagged, immutable release referencing a known source SHA and PDF digest after acceptance. |
| P1 | **Exact-source rerun** | On a clean checkout, rerun `python -m unittest discover -v`, `python scripts/run_stress_tests.py --check verification/stress_test_results.json`, synthetic pilot baseline comparison, and the pinned Lean build/audits. Archive executable, toolchain, exit status and hash evidence. Earlier 48/48 owner-local tests are not a new release-run receipt. |
| P1 | **PDF and source package** | Rebuild the manuscript on the exact frozen commit, inspect warnings, all pages and key tables/figures; verify references, PDF metadata, byte hash and a clean arXiv-compatible TeX source package. The accepted PDF is not a guarantee that a later arXiv build succeeds. |
| P1 | **External reviews and response log** | Obtain at least one mathematical/formal reviewer and one cybersecurity measurement reviewer; obtain a statistical-methods reviewer if feasible. Track each objection, severity, response and revision before author signoff. |
| P2 | **Venue and license** | Confirm topical fit, page limit, format, preprint policy, journal expectations and any arXiv endorsement. arXiv moderation and posting are **not** peer review; choose rights/license knowingly. |

## Recommended decision sequence

1. **Now:** circulate the accepted foundation manuscript as a **pre-submission review draft** with the [referee packet](CRPI_EXTERNAL_REFEREE_PACKET.md). No organizational pilot consent is required for a review of already public synthetic research.
2. **Before public preprint:** resolve P0 scientific critiques, author metadata, stable version, clean build, current runtime checks, and license. Record explicit author approval.
3. **Preprint route:** prepare arXiv `cs.CR` subject to moderation/endorsement/compilation checks, or select another appropriate preprint outlet. Never describe posting as peer review.
4. **Peer-reviewed route:** select a journal or workshop only after checking whether a 41-page primarily theoretical/methodological paper fits scope and empirical-review expectations; shorten or create an expanded companion as necessary.
5. **Separately:** continue [Issue #9](https://github.com/jmsbooth/cyber-risk-posture-model/issues/9) for authorized organizational measurement validity, independent outcomes and prospective utility. Report empirical nulls and negative results; do not retrofit unverified effects into this foundation paper.

## Hard prohibitions

- Do not contact organizations, submit a manuscript, assert institutional affiliation, accept an irreversible license, or identify actual reviewers without author approval.
- Do not place confidential organizational inventories, incidents, credentials, personal identifiers or approval documents in this public repository.
- Do not lower or bypass `--require-ready` on the study preflight, or confuse a peer-referee review with a field-validity study.

**Tracking:** [Issue #12 — external review and release](https://github.com/jmsbooth/cyber-risk-posture-model/issues/12); [Issue #9 — empirical pilot](https://github.com/jmsbooth/cyber-risk-posture-model/issues/9).
