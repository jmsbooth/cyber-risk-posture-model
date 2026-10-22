# Phase C proof status — Verified, conditional persistence/cadence claims

Protocol: [CRPI-FVP-001](../../docs/FORMAL_VERIFICATION_PROTOCOL.md)  
Phase B's [24 conditional proofs are verified and merged](PHASE_B_STATUS.md) in PR #2. The accepted Phase A proofs are unchanged. Phase C PR #3 is now based on `main`.  
**Status: PHASE C VERIFIED — 21 theorem statements under the explicitly stated mathematical hypotheses.** The [exact-revision machine-check evidence](../../verification/evidence/9dab18ba0e7045c28754746a0ba61a2cb1d2e592/phase-c-summary.json) has been committed and reviewed. For mathematical source `9dab18ba0e7045c28754746a0ba61a2cb1d2e592`, the owner-local pinned **Lean 4.24.0** and Mathlib `f897ebcf72cd16f89ab4577d0c826cd14afaafc7` build passed (**7,359 jobs**) and all **21 theorem axioms** were audited with exit code zero. Each theorem uses only `propext`, `Classical.choice` and `Quot.sound`. Manifest SHA-256: `c3c1ac12354571388bf36c1532f77dfe9ffa7cac846f786b479b3c072d10e308`. The [correspondence review](PHASE_C_STATEMENT_REVIEW.md) passed for the exact stock-transition and cadence claims. Only documentation/evidence changed after the tested source commit. The two reported unused-hypothesis warnings are in already accepted Phase B source and are nonblocking.

## Manuscript alignment and proof scope

| Claim | Candidate Lean theorem | Goal | Status |
| --- | --- | --- | --- |
| P3 | `totalRate_nonneg` / `zero_totalRate_zero_terms` | Nonnegative rates and degenerate no-update case | **Verified (Phase C; conditional)** |
| P3 | `stockDrift_affine`, `stockDrift_lower_boundary_nonneg`, `stockDrift_upper_boundary_nonpos`, `stockDrift_zero_iff_equilibrium` | Exact ODE drift, inward boundaries, unique equilibrium when q>0 | **Verified (Phase C; conditional)** |
| P3 | `stockEquilibrium_bounded` | Equilibrium in [0,1] when total rate positive | **Verified (Phase C; conditional)** |
| P3 | `decayFactor_bounded` | Exponential factor in (0,1] for nonnegative elapsed time and rate | **Verified (Phase C; conditional)** |
| P3 | `intervalStep_bounded` | Convex-combination invariant | **Verified (Phase C; conditional)** |
| P3 | `stockTransition_zero_rate` / `stockTransition_bounded` | Exact update with q=0 branch preserves state and [0,1] | **Verified (Phase C; conditional)** |
| P3 | `intervalStep_equilibrium` / `stockTransition_equilibrium` | Fixed equilibrium under constant inputs | **Verified (Phase C; conditional)** |
| P3 | `intervalStep_contraction` | Absolute distance to equilibrium never increases | **Verified (Phase C; conditional)** |
| P3 | `intervalStep_decreases_above` / `intervalStep_increases_below` | Directional evolution toward equilibrium for longer intervals | **Verified (Phase C; conditional)** |
| P3 | `intervalStep_tendsto_equilibrium` / `stockTransition_tendsto_equilibrium` | Convergence as elapsed time tends to infinity when q>0 | **Verified (Phase C; conditional)** |
| P4 | `intervalStep_semigroup` / `stockTransition_semigroup` | Exact cadence consistency with identical interval rates and inputs | **Verified (Phase C; conditional)** |
| P6 complement | `envelope_after_transition_bounded` | CRPI envelope boundedness using verified P3 stock invariance | **Verified (Phase C; conditional)** |

The definitions use exactly:

```text
a = beta * R_inst
b = kappa * M
q = a + b
S_star = a / q          (only when q > 0)
T(dt, S) = S_star + (S - S_star) * exp(-q * dt)
q = 0 => T(dt, S) = S
```

No proof substitutes an Euler discretization, resets historical stock each
step, or treats the rates as dimensionless. `Real.exp ((-q) * dt)` is
mathematically the same as `exp(-q * dt)` used in the manuscript. The cadence
statement requires identical inputs on the adjacent intervals. A general
time-varying ODE existence/uniqueness proof is deliberately out of scope.

## Final acceptance

1. **Source-to-paper correspondence:** PASS for Proposition 3's exact piecewise-constant stock dynamics, Proposition 4's same-input cadence semigroup, and the bounded-envelope continuation of Proposition 6; refer to [the statement review](PHASE_C_STATEMENT_REVIEW.md).
2. **Machine check:** PASS for all 21 listed theorem declarations, with exact source revision and toolchain attested by the [archived evidence](../../verification/evidence/9dab18ba0e7045c28754746a0ba61a2cb1d2e592/phase-c-summary.json).
3. **Source integrity:** GitHub comparison `9dab18ba...` to acceptance head shows only this proof documentation and the three archived logs, with no Lean theorem, dependency or toolchain changes.
4. **Mathematical limitations:** The general time-varying ODE, dimensionally typed quantities, Proposition 6 envelope-switch nondifferentiability and Phase D Python-reference conformance are **not** proven by this phase. All stock invariant statements depend on bounded residual/mitigation and nonnegative rates and duration.
5. **Decision:** Phase C is eligible for merge. Do not claim numerical implementation conformance or a blanket formal proof of the entire manuscript until the remaining protocol gates are satisfied.

### Reproduce the proof

From `formal/lean` in the pinned local toolchain:

```bash
lake build
lake env lean CRPI/AuditC.lean
```

The PowerShell collector at repository root, `scripts/capture_phase_c.ps1`, captures exact-revision build and axiom evidence in `verification/evidence/<source-commit>/`.
