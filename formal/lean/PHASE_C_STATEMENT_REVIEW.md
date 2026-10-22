# CRPI Phase C — Theorem-to-Manuscript Correspondence Review

**Date:** 2026-10-22  
**Protocol:** [CRPI-FVP-001](../../docs/FORMAL_VERIFICATION_PROTOCOL.md)  
**Review basis:** [CRPI manuscript Governing Model and Analytical Properties](../../paper/CRM_revised.tex), [Phase C Persistence.lean](CRPI/Persistence.lean), [21-target axiom audit](CRPI/AuditC.lean).  
**Source revision reviewed:** `fcbc6026e34fee75d8f4c26374c1e6ada3160b81` (includes unchanged persistence theorem source from earlier candidate commits).

**Statement correspondence: PASS for the documented Phase C candidate scope. Machine-check status: NOT RUN.** This is an independent review of intended theorem statements and hypotheses, **not** a report that Lean has accepted any Phase C theorem. The compiler and axiom audit may still reveal errors.

## Governing equation and rate semantics

The source retains the paper's affine stock-flow equation exactly:

`dS/dt = beta * R_inst * (1 - S) - kappa * M * S`

It defines `a = beta * R_inst`, `b = kappa * M`, `q = a+b` and (for `q>0`) `S_star = a/q`. The exact piecewise-constant interval update is `S_star + (S - S_star) * exp(-q*dt)`; for `q=0` the state is unchanged. Nothing substitutes Euler integration or resets stock between intervals. Units are represented by the manuscript's choice of rates per time and `dt` as elapsed time, but dimensional typing is not formalized.

## Theorem-to-proposition review

| Paper claim | Candidate Lean statement(s) | Mathematical correspondence |
| --- | --- | --- |
| P3 — affine ODE and inward boundaries | `stockDrift_affine`, `stockDrift_lower_boundary_nonneg`, `stockDrift_upper_boundary_nonpos` | **Matches.** Boundary checks assume nonnegative applicable rates and bounded residual/mitigation; these prove drift signs at S=0 and S=1, not a general ODE invariance theorem. |
| P3 — unique equilibrium | `stockDrift_zero_iff_equilibrium`, `stockEquilibrium_bounded` | **Matches.** With `q>0`, drift equals zero if and only if stock equals `a/q`; that equilibrium is in [0,1] under the physical input bounds. |
| P3 — zero-rate case | `totalRate_nonneg`, `zero_totalRate_zero_terms`, `stockTransition_zero_rate` | **Matches.** With nonnegative rates and bounded inputs, `q=0` forces both contribution terms to zero and makes the exact update the identity. |
| P3 — bounded persistence | `decayFactor_bounded`, `intervalStep_bounded`, `stockTransition_bounded` | **Matches.** For `dt≥0` and `q≥0` the exponential factor is in (0,1], and the updated stock is a convex combination of the previous stock and bounded equilibrium. |
| P3 — approach and convergence | `intervalStep_equilibrium`, `stockTransition_equilibrium`, `intervalStep_contraction`, `intervalStep_decreases_above`, `intervalStep_increases_below`, `intervalStep_tendsto_equilibrium`, `stockTransition_tendsto_equilibrium` | **Matches.** The fixed point is unchanged, distance to equilibrium does not grow, and the exponential solution converges as time increases when `q>0`. The convergence theorem is for the constant-input exact transition, not a general time-varying ODE. |
| P4 — cadence consistency | `intervalStep_semigroup`, `stockTransition_semigroup` | **Matches.** Two adjacent intervals use exactly the same `beta`, `kappa`, residual and mitigation inputs. The equality must not be interpreted as cadence invariance when these inputs change or when elapsed time differs. |
| P6 — post-update envelope boundedness | `envelope_after_transition_bounded` | **Matches.** Combines the existing `max` envelope with stock preservation under valid bounded initial state, nonnegative duration and rates. Does not establish envelope non-differentiability at the switching boundary. |

## Critical limitations and proof policy

- Lean statements about the exact transition are not equivalent to formal verification of all solutions of the nonautonomous, time-varying stock-flow ODE. That generalization is explicitly out of scope.
- P3 includes analytic uniqueness and boundedness of the fixed equilibrium. Empirical correctness or calibration of `beta` and `kappa` remains separate.
- The cadence theorem is an algebraic semigroup under identical interval inputs. It does not assert invariance under arbitrary observation frequency, missing telemetry, or changing calibration.
- The P6 extension assumes that the supplied instantaneous residual is already in [0,1], which is covered by the earlier conditional Phase A model equations.
- Source inspection found no deliberate weaker surrogate replacing the manuscript's rate or exact-update equations. This review does not establish that Lean tactics or imported lemmas compile; that remains a blocking next step.

**Acceptance:** Keep [Phase C PR #3](https://github.com/jmsbooth/cyber-risk-posture-model/pull/3) in draft. Run the pinned Lean/Mathlib project build, resolve any proof errors without altering model mathematics, audit all 21 theorem declarations, inspect exact-revision evidence, and merge only after Phase B's verified prerequisite is merged and the protocol's conditional claims are qualified.
