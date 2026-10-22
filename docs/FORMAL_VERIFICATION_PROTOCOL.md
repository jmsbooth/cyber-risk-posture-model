# CRPI Formal Verification Protocol

**Protocol ID:** CRPI-FVP-001  
**Version:** 0.1.4  
**Status:** Bounded mathematical verification and numerical reference conformance accepted; manuscript PDF publication gate open  
**Date:** 2026-10-22  
**Repository:** [jmsbooth/cyber-risk-posture-model](https://github.com/jmsbooth/cyber-risk-posture-model)  
**Source baseline:** `main` at `6752d3a32162848bcd73b6274a90b6e2442f163a` (manuscript and Python reference implementation)  
**Owner:** Repository maintainer

**Implementation status (2026-10-22):** [Phase A](../formal/lean/PROOF_STATUS.md) has 11 verified conditional theorem statements with [accepted build/axiom evidence](../verification/evidence/b50dea4aaf40cad56c42cff436d450278459efbf/summary.json). [Phase B](../formal/lean/PHASE_B_STATUS.md) has 24 verified conditional statements for Proposition 1 and Proposition 5 with [accepted build/axiom evidence](../verification/evidence/e457153dc5ac5b48b432b3a6fec57d492432b1bb/phase-b-summary.json) and an independent manuscript correspondence review. [Phase C](../formal/lean/PHASE_C_STATUS.md) has 21 verified conditional statements for persistent stock, equilibrium, convergence and exact cadence, supported by [archived source-matched evidence](../verification/evidence/9dab18ba0e7045c28754746a0ba61a2cb1d2e592/phase-c-summary.json). The three accepted phases comprise 56 machine-checked theorem declarations, each bounded by its documented hypotheses. Phase D [numerical conformance evidence](../verification/evidence/509c5ae448cddbcd062ad8c984c713d73c07c345/phase-d-summary.json) is accepted: Python 3.11.15, 19/19 tests, 44 Decimal oracle fields, 5 invariants, 25 scenario rows, and 56/56 theorem audits at source revision `509c5ae448cddbcd062ad8c984c713d73c07c345`. The [P1–P6 matrix](../verification/PROOF_COVERAGE_MATRIX.md) qualifies the six propositions' required subclaims and retains all boundaries. Version 0.1.4 changes implementation status only; trust and acceptance policies are unchanged. A separate verified manuscript PDF build/publication check remains open.

## 1. Purpose and verification boundary

This protocol defines how CRPI mathematical claims will be translated into Lean 4, machine-checked, compared against the executable Python reference implementation, documented, and accepted. It is deliberately a **bounded verification protocol**, not a redesign program or a claim that the cyber-risk model has been empirically established.

Keep four forms of evidence distinct:

| Activity | Establishes | Does **not** establish |
| --- | --- | --- |
| Analytical proof in the paper | A mathematical argument under written assumptions | That Lean checked it |
| Lean 4/Mathlib verification | The precisely formalized statement has a kernel-accepted proof under explicit hypotheses and audited dependencies | Correctness of measurements, chosen parameters, or cyber-risk semantics in the real world |
| Python/reference-vector conformance and synthetic tests | The implementation behaves consistently with agreed numerical examples and interfaces, within declared tolerance | A proof over all real inputs or empirical utility |
| Empirical research | Whether the model usefully explains, discriminates, or informs decisions on observed outcomes | A substitute for the formal mathematical proof |

**Language gate:** Do not describe CRPI as "Lean-verified," "formally verified," or "machine-checked" until the relevant statements build, the proof audit is complete, and the exact theorem coverage is published. Even then, say **"selected mathematical invariants of the CRPI governing equations have been machine-checked under stated assumptions."** Do not claim validated breach probabilities, calibrated losses, parameter accuracy, or empirical superiority.

## 2. Authority and change control

1. **Human-readable equation specification:** [`paper/CRM_revised.tex`](../paper/CRM_revised.tex), especially the Governing Model and Analytical Properties appendix.
2. **Executable reference:** [`models/crm_reference.py`](../models/crm_reference.py) (its legacy filename does not change the CRPI construct).
3. **Illustrative parameter interface:** [`config/calibration_baseline.json`](../config/calibration_baseline.json).
4. **Independent mathematical formalization:** the Lean definitions to be added under `formal/lean/`. Lean must be authored from the manuscript mathematics, not generated or translated blindly from Python.
5. **Conformance evidence:** reference vectors and regression tests, created in a later implementation increment.

Freeze the current functional forms for `G_epsilon`, `CS`, `R_j`, `D_eff`, `H`, `M`, `R_inst`, the persistence transition, and `CRPI = max(R_inst, S)`. Maintain the single mitigation variable `M`; do not split preventive and remediative mitigation as part of verification.

**No proof-driven model substitution.** If a claimed property cannot be proved as stated, classify the result as (a) missing hypothesis, (b) false claim/counterexample, (c) formalization mismatch, or (d) unresolved proof-engineering problem. Record the precise finding. Do not silently change the theorem, redefine an operator, strengthen assumptions, or alter the paper/Python mathematics just to make Lean accept it. Any substantive correction requires a separate documented model-change decision and synchronized source updates.

The formalization must distinguish **real-valued mathematical semantics** from **floating-point implementation behavior**. Python's numerical tolerances, clamping for roundoff, finite-precision exponentials, and approximate reference values are conformance topics, not Lean theorem premises.

## 3. Initial proof scope: six manuscript propositions only

The first formal-verification milestone covers the existing six analytical propositions and their immediate supporting lemmas. Use the paper's definitions exactly; keep theorem hypotheses visible in the signatures.

| Paper claim | Required Lean property | Phase | Initial status |
| --- | --- | --- | --- |
| P1 — regularized geometric aggregation | Output boundedness; all-zero/all-one endpoints; coordinate monotonicity; zero-weight irrelevance | B | Not started |
| P2 — consequence, hazard, mitigation | Bounds for domain projections, `D_eff`, `H`, `M`, and `R_inst` | A/B | Not started |
| P3 — persistence invariance/equilibrium | `q=0` identity; valid equilibrium when `q>0`; bounded exact update; movement toward equilibrium; convergence under constant inputs | C | Not started |
| P4 — cadence consistency | Exact transition semigroup for adjacent nonnegative durations **with unchanged inputs and rates** | C | Not started |
| P5 — directional sensitivity | Non-decreasing response to `TE` and consequence; non-increasing response to applicable resilience, `CM`, and `USOM`, with other variables fixed | B | Not started |
| P6 — CRPI envelope | Bounded `max(R_inst,S)` and monotonicity in its arguments | A | Not started |

The **Initial status** column documents the original October 21 baseline. It is intentionally historical; the [current proof ledger](../formal/lean/PROOF_STATUS.md), not this table, governs live claim acceptance. Phases A–C now provide the required conditional mathematical counterparts of P1–P5 and P6 boundedness/monotonicity; the optional P6 nondifferentiability property and general nonautonomous ODE proof remain out of scope. Phase D's [Python numerical conformance](../verification/PHASE_D_STATUS.md) is now accepted, with the final manuscript PDF regeneration explicitly not run.

### Explicit mathematical conditions

- Every score and normalized primitive is in `[0,1]`.
- Aggregation weights are **nonnegative**, sum to one, and may be zero. Do not assert strict monotonicity for a zero-weight term.
- Regularization satisfies `0 < epsilon < 1`; denominator and logarithm/power operations must have valid domains. For the zero-safety claim, "one zero does not annihilate the result" requires at least one **other positively weighted, positive-valued** component.
- Consequence weights `v_j` and resilience projection weights `a_ji` are nonnegative and normalized; `rho_j`, `m0`, `CM`, `USOM`, `TE`, `D_j`, and `R_j` are bounded.
- Rates `beta`, `kappa` and interval duration `dt` are nonnegative, with matching declared time units.
- `q = beta * R_inst + kappa * M`. For `q > 0`, define the equilibrium `S_star` and exact interval transition as in the manuscript. For `q = 0`, transition is identity.
- The transition is proved for **piecewise-constant inputs over each interval**. The cadence/semigroup theorem compares intervals with the **same** `R_inst`, `M`, `beta` and `kappa`; it does not assert that changing measurement sampling while the inputs change has no effect.
- Scope levels are alternative evidence boundaries, not an implicit proof that averaging child indices equals a parent CRPI. No cross-scope comparability theorem is included.

### What is deliberately out of scope

Do not make the v0.1 gate depend on a general ODE existence/uniqueness formalization; prove the exact interval transition first. The paper may explain the stock-flow ODE analytically, but a transition theorem must not be presented as a Lean proof of every time-varying ODE solution. Formal non-differentiability of the `max` envelope is optional; its boundedness and monotonicity are required.

Do not formalize the statistical calibration pipeline, evidence provenance, coverage-label policy, Monte Carlo methods, AI-era trend attribution, organizational roll-ups, or empirical validity in this milestone. These have separate measurement and validation workstreams.

## 4. Trusted computing base and prohibited shortcuts

Use Lean 4 with Mathlib, compiled and checked by Lean's kernel. Pin the toolchain and dependencies using `formal/lean/lean-toolchain`, `formal/lean/lakefile.toml` (or an equivalent Lake configuration), and the committed `formal/lean/lake-manifest.json`. Dependency upgrades must be explicit, reviewed, and independently rebuilt; an unpinned "latest" toolchain is not acceptable for the release artifact.

**A theorem counts as verified only when its full stated type is checked and the trusted assumptions are audited.**

Rules for theorem-bearing code on the accepted branch:

- No `sorry`, `admit`, project-defined `axiom`, `unsafe` proof dependencies, `native_decide`, or unchecked external proof oracles.
- Existing Lean/Mathlib foundational axioms (for example classical choice or propositional extensionality when genuinely required) may be used **only if disclosed through an axiom audit**. "No new axioms" does not mean pretending foundational axioms do not exist.
- No opaque replacement of the actual model definition by an easier surrogate. Auxiliary lemmas and mathematically equivalent rewrites are permitted only with a checked equivalence bridge.
- Standard kernel-checking tactics (`simp`, `ring`, `linarith`, `nlinarith`, `positivity`, `field_simp`, etc.) are permitted. A tactic succeeding does not waive theorem-type or assumption review.
- Check `#print axioms` (or an equivalent theorem-assumption report) for every public theorem, not merely successful compilation. Record unexpected assumptions as a blocking finding.
- Working branches may contain incomplete experiments; unproved declarations must not enter the accepted formalization or be labeled "proved." Proof status may instead be recorded as **Open** in documentation.

A source scan for prohibited constructs is a safeguard, **not** a substitute for compilation, kernel checking, and manual statement review.

## 5. Required implementation structure

Keep the repository's existing `paper/`, `models/`, `config/`, `scripts/`, and `tests/` layout. Add only the bounded formal-verification surface:

~~~text
formal/lean/
  lakefile.toml
  lean-toolchain
  lake-manifest.json
  CRPI/
    Basic.lean
    Aggregation.lean
    Consequence.lean
    Mitigation.lean
    Persistence.lean
    Envelope.lean
    Main.lean
  README.md
  PROOF_STATUS.md

verification/
  reference_vectors.json
  evidence/
    <verified-revision>/
      summary.json
      proof-audit.md
~~~

The file names are organizational guidance; exact theorem names may follow Lean conventions. Keep the proof modules small, composable, and importable under a single `lake build` target. `Main.lean` should import all required theorem modules so an apparently successful build cannot accidentally omit a proof file.

The reference-vector file is a numerical **conformance artifact**, not an alternative mathematical specification. Include known intermediates (at least `R_j`, `CS`, `D_eff`, `H`, `M`, `R_inst`, `S_next` and `CRPI`), edge cases, and the manuscript's worked example. Store exact rational or decimal test inputs and declared floating-point tolerances; avoid making hand-rounded table values the only oracle.

## 6. Execution sequence and stop rules

Work in four bounded increments. Each increment is independently reviewable and must report completed, open, and blocked claims.

**A — Environment and elementary bounds.** Pin Lean/Mathlib; create the actual equation definitions, nonnegative/bounded real-value hypotheses, and a verified project build. Prove `CRPI` envelope bounds, weighted-sum bounds, and the elementary consequence/mitigation/residual bounds. Map Lean names to propositions.

**B — Aggregation and directional behavior.** Prove the general finite-input regularized geometric operator, zero-weight invariance, endpoint properties, resilience projections, and monotonic effects. Preserve the correct hypotheses for non-strict versus strict statements. Use a finite index type or finite set rather than proving only the two-element example and claiming generality.

**C — Persistence and temporal behavior.** Prove equilibrium conditions, the `q=0` branch, exact-update boundedness, monotone approach to equilibrium, convergence for constant inputs, and the cadence semigroup. Make the interval assumptions explicit in theorem names/docstrings.

**D — Independent conformance and publication.** Build canonical reference vectors, test Python's numerical implementation against them and the manuscript's worked series, regenerate the manuscript's reproducible calculations, run the Lean axiom/source audits, and publish the exact proof-status matrix.

**Boundedness rule:** Do not allow one difficult Mathlib lemma or a generalized ODE project to block the entire research effort. After one focused proof increment without a viable approach, document the exact statement, attempted approach, failure, and next candidate lemma; classify it **Open/Blocked**, continue other claims, and report partial coverage accurately. A claim with a weaker proved theorem is **Partial**, not **Verified**. No undocumented assumption strengthening or feature creep.

Each formalization change starts with a written statement-to-paper mapping; then add definitions, prove supporting lemmas, run Lean, audit assumptions, run numerical conformance where applicable, and update the proof ledger. Never write the manuscript's "machine-checked" claim ahead of the actual result.

## 7. Verification commands and reproducible evidence

After the Lean package is created, the primary local workflow is:

~~~bash
cd formal/lean
lake exe cache get
lake build
~~~

The Mathlib cache speeds local work; cached artifacts do not replace a successful Lean build with the pinned manifest. For the existing Python and scenario checks, run from the repository root:

~~~bash
python3 -m unittest discover -v
python3 scripts/validate_model.py
python3 scripts/run_scenarios.py
tectonic --outdir paper/build paper/CRM_revised.tex
~~~

If any tool is unavailable, mark its check **Not run** with the reason; never mark it passed by inference. The eventual single-command local verification entry point may orchestrate these commands, but it must preserve exit codes and fail on any required failed check.

Because hosted CI is optional, **a witnessed local/manual verification run is an accepted release mechanism** when GitHub Actions is unavailable or has no credits. Commit a small, non-sensitive evidence summary for the exact tested commit or tree; keep large generated build outputs and caches out of Git.

Every evidence record must include:

- exact Git commit SHA/tree revision and CRPI specification/profile version;
- Lean version, Mathlib revision, Lake manifest identity, and platform;
- executed commands, exit codes, and UTC verification timestamp;
- all public theorem names, corresponding paper propositions, theorem-level status, and axiom audit;
- Python regression/reference-vector results and manuscript build status where run;
- documented numerical tolerances, unresolved gaps, and whether the evidence is **partial** or **release-qualified**.

**Stale evidence rule:** An evidence record for an older source or dependency revision does not certify a later revision. Re-run affected gates when definitions, hypotheses, Lean dependencies, Python reference equations, or manuscript equations change. Documentation-only changes may use a scoped verification record explaining why mathematical gates are unaffected.

## 8. Proof ledger, review, and acceptance gate

Use `formal/lean/PROOF_STATUS.md` as the human-readable ledger. For every claimed result record:

| Field | Required content |
| --- | --- |
| Claim | Manuscript proposition/subclaim and section |
| Formal object | Fully qualified Lean definition and theorem names |
| Hypotheses | Bounded domains, weight conditions, positivity, constancy, scope |
| Status | Planned / Open / Blocked / Partial / Verified |
| Trust audit | Recorded assumptions from `#print axioms` |
| Evidence | Exact passing revision and local run record |
| Limits | What the theorem does not establish |

Before promoting a theorem to **Verified**, confirm: (1) it matches the actual manuscript formula rather than a substituted model; (2) its hypotheses do not remove relevant boundary cases; (3) Lean compiles it in the complete project build; (4) no prohibited placeholders or unreviewed axioms remain; and (5) the trust audit and evidence are linked.

The **full formal-verification milestone** may be released only when all six propositions have verified counterparts for their stated required subclaims, the numerical conformance gate passes, and the corresponding paper/repository proof status is synchronized. Otherwise publish a **partial formalization** with the open claims visible and no blanket verification language.

Repository-owner review of this protocol is permitted after publication. Amend its version and document any subsequent decisions rather than retroactively implying earlier verification met new requirements.

## 9. Manuscript and publication wording

Until proof completion, leave the paper's analytical appendix as analytical argument and describe Lean as **planned** or **in progress**, not completed. Once the verified claims and exact revision have been confirmed, add a short subsection to the Verification and Reproducibility material with the pinned Lean/Mathlib version, artifact path, theorem coverage, and open limitations.

Permitted wording after a successful full gate:

> Selected boundedness, aggregation, directional, persistence-transition, and envelope properties of the CRPI v0.1 governing equations were independently formalized and machine-checked in Lean 4/Mathlib under explicitly stated assumptions. This does not establish parameter calibration, measurement or construct validity, incident prediction, or empirical superiority.

Never call a transition-function proof a machine-checked proof of general time-varying ODE behavior. Do not describe passing Lean proofs or synthetic simulations as empirical validation.

## 10. Exit criteria and handoff

**Protocol-publication milestone (this change):** The protocol is committed on `main`, linked from `README.md`, and available for owner review. This is a **process artifact only**. It does not mark any proposition Verified.

**Lean-verification milestone (subsequent increments):** Pinned reproducible Lean build; complete proof ledger and trust audit; each accepted theorem checked against the paper; independent Python/reference-vector conformance; exact-revision local evidence; and appropriately qualified manuscript wording. Tag a formal-spec release only after these gates pass.

Afterward, prioritize sensitivity/identifiability, stateful uncertainty propagation, simple additive baseline comparison, and observational/prospective empirical validation as separate research tracks. Formal verification must not be used to defer those empirical questions or to make stronger claims than the proofs support.

### Reference toolchain documentation

- [Lean 4 / Lake](https://github.com/leanprover/lean4/tree/master/src/lake)
- [Mathlib 4 and precompiled-cache workflow](https://github.com/leanprover-community/mathlib4)
