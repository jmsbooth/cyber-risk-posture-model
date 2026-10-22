# CRPI Phase B — Theorem-to-Manuscript Correspondence Review

**Date:** 2026-10-22  
**Protocol:** [CRPI-FVP-001](../../docs/FORMAL_VERIFICATION_PROTOCOL.md)  
**Candidate proof source revision:** `e457153dc5ac5b48b432b3a6fec57d492432b1bb`  
**Reviewed sources:** [manuscript governing equations and appendix](../../paper/CRM_revised.tex), [aggregation proofs](CRPI/Aggregation.lean), and [direction proofs](CRPI/Direction.lean).

**Statement-to-manuscript decision: PASS for Proposition 1 and Proposition 5 in their stated mathematical scope.** This is a theorem-type review, distinct from empirical validity. The owner-local Lean 4.24.0 [build and 24-target axiom audit](../../verification/evidence/e457153dc5ac5b48b432b3a6fec57d492432b1bb/phase-b-summary.json) have now been committed and independently inspected, completing the separate machine-check acceptance requirement.

## Proposition 1 — Regularized geometric aggregation

| Manuscript property | Lean object / theorem | Correspondence and limits |
| --- | --- | --- |
| Finite weighted product | `regularizedBase`, `regularizedProduct`, `regularizedGeometric` | **Matches** (product of [epsilon+(1-epsilon)x] raised to each weight, minus epsilon, divided by 1-epsilon). A finite index set can represent arbitrary finite governed domains. |
| Base and output bounds | `regularizedBase_bounds`, `regularizedProduct_bounds`, `regularizedGeometric_bounded` | **Matches.** Assumes 0<epsilon<1, bounded inputs, nonnegative weights summing to one. |
| All-zero / all-one endpoints | `regularizedGeometric_zero`, `regularizedGeometric_one` | **Matches.** The all-one proof uses weaker hypotheses because each factor is already one. |
| Zero weights | `regularizedProduct_zero_weight_irrelevance`, `regularizedGeometric_zero_weight_irrelevance` | **Matches.** Changing only zero-weight coordinates leaves the aggregate unchanged. |
| Weak monotonicity | `regularizedGeometric_mono` | **Matches.** Componentwise input order; other weights and epsilon unchanged; nonnegative weights. |
| Strict positive-weight monotonicity | `regularizedGeometric_strictMono` | **Matches.** At least one positively weighted input strictly improves and no other input decreases. |
| No absorbing zero | `regularizedGeometric_pos_of_positive_component` | **Matches.** A positively weighted positive input suffices for strictly positive output, even if other inputs are zero. |
| Consequence-specific resilience | `domainResilience`, `domainResilience_bounded` | **Matches.** Uses the same regularized geometric operator with domain-specific weights. |

The manuscript gives a derivative expression to support monotonicity. The formal proof instead establishes input-order inequalities; it does **not** separately machine-check the derivative identity. Those order theorems prove the paper's stated monotonicity conclusion without substituting a different governing function.

## Proposition 5 — Directional sensitivity

| Manuscript claim | Lean theorem(s) | Review |
| --- | --- | --- |
| Higher domain consequence does not lower adjusted consequence | `effectiveConsequence_mono_domain` | **Matches.** Nonnegative consequence weights, bounded resilience and mitigability. |
| Higher domain resilience does not increase adjusted consequence | `effectiveConsequence_antitone_resilience` | **Matches.** Nonnegative weights, consequences and domain mitigability. |
| Higher TE/consequence does not lower hazard | `hazard_mono_threat`, `hazard_mono_consequence` | **Matches.** Multiplicative monotonicity under nonnegative factors. |
| Higher USOM/CM does not reduce mitigation | `mitigation_mono_usom`, `mitigation_mono_cm` | **Matches.** Fixed m0 and nonnegative control factors. |
| Higher hazard/mitigation changes residual as claimed | `instantaneousResidual_mono_hazard`, `instantaneousResidual_antitone_mitigation` | **Matches.** Appropriate nonnegative hazard and bounded mitigation. |
| Composed instantaneous residual has claimed directions | `currentResidual_mono_threat`, `currentResidual_mono_domain`, `currentResidual_antitone_resilience`, `currentResidual_antitone_usom`, `currentResidual_antitone_cm` | **Matches.** Composes exactly the manuscript D_eff, H, M and R_inst equations; scalar RRAS is not inserted. |

Some Lean monotonicity statements use fewer domain restrictions than the paper's valid input range; this is a stronger mathematical statement, **not** a license to feed unvalidated inputs into CRPI. The direction theorems do not claim that all the manuscript's partial derivatives were independently proved in Lean or that time-varying persistent stock and the final CRPI envelope have those same directions.

## Verification evidence and release gate

1. **Local execution reported:** Source `e457153dc5ac5b48b432b3a6fec57d492432b1bb`, successful `lake build` (7,358 jobs), and successful `scripts/capture_phase_b.ps1` with pinned Lean 4.24.0 and 24 theorem audit targets. The script accepts only standard declared foundational axioms.
2. **Two nonblocking warnings:** Unused hypotheses `hε0` in `regularizedBase_bounds` and `hε1` in `regularizedGeometric_zero`. Neither is a missing proof, but changing them would alter theorem source and require another exact-revision build. Keep the checked code intact for this evidence.
3. **Evidence archived:** The exact source-revision `verification/evidence/e457153dc5ac5b48b432b3a6fec57d492432b1bb/` includes [summary](../../verification/evidence/e457153dc5ac5b48b432b3a6fec57d492432b1bb/phase-b-summary.json), successful build log, 24 theorem axiom reports, pinned compiler, dependency revision and manifest hash. This satisfies the artifact gate for the reviewed mathematical source.
4. **No proof shortcuts:** Source review found no `sorry`, `admit`, custom `axiom`, `unsafe` proof dependencies or `native_decide`.
5. **Out of scope:** Phase C temporal invariance/equilibrium/cadence and Phase D manuscript/Python conformance remain unverified. Empirical calibration/validity remains a separate research concern.

**Final decision:** The Proposition 1 and 5 statement correspondence review **passes**, and the source-matched machine-check record is archived. The 24 conditional theorem claims are **Verified** in their mathematical scope; Phase B may merge. The derivative equations, unproved persistence dynamics, Python numerical conformance and empirical validity are explicitly excluded.
