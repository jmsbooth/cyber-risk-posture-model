# Phase C proof status — candidate, unverified

Protocol: [CRPI-FVP-001](../../docs/FORMAL_VERIFICATION_PROTOCOL.md)  
This branch is stacked atop Phase B, whose proofs are also **pending** real
machine-checking. The accepted Phase A proofs are unchanged.  
**Status: PREPARED ONLY. No Phase C `lake build`, axiom audit, or evidence has run.**

## Manuscript alignment and proof scope

| Claim | Candidate Lean theorem | Goal | Status |
| --- | --- | --- | --- |
| P3 | `totalRate_nonneg` / `zero_totalRate_zero_terms` | Nonnegative rates and degenerate no-update case | Open |
| P3 | `stockEquilibrium_bounded` | Equilibrium in [0,1] when total rate positive | Open |
| P3 | `decayFactor_bounded` | Exponential factor in (0,1] for nonnegative elapsed time and rate | Open |
| P3 | `intervalStep_bounded` | Convex-combination invariant | Open |
| P3 | `stockTransition_zero_rate` / `stockTransition_bounded` | Exact update with q=0 branch preserves state and [0,1] | Open |
| P3 | `intervalStep_equilibrium` / `stockTransition_equilibrium` | Fixed equilibrium under constant inputs | Open |
| P3 | `intervalStep_contraction` | Absolute distance to equilibrium never increases | Open |
| P3 | `intervalStep_decreases_above` / `intervalStep_increases_below` | Directional evolution toward equilibrium for longer intervals | Open |
| P3 | `intervalStep_tendsto_equilibrium` / `stockTransition_tendsto_equilibrium` | Convergence as elapsed time tends to infinity when q>0 | Open |
| P4 | `intervalStep_semigroup` / `stockTransition_semigroup` | Exact cadence consistency with identical interval rates and inputs | Open |
| P6 complement | `envelope_after_transition_bounded` | CRPI envelope boundedness using verified P3 stock invariance | Open |

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

## Verification acceptance

1. All Lean source **and Phase B dependencies** compile with the pinned Lean
   4.24.0/Mathlib4 versions.
2. All **17 Phase C declarations** are checked and appear in
   `lake env lean CRPI/AuditC.lean` without unexpected axioms.
3. Review the theorem statements, mathematical assumptions, and correspondence
   against the manuscript's Proposition 3, Proposition 4 and the conditional
   Proposition 6.
4. Commit exact-revision `verification/evidence/<commit>/` proof and axiom logs.
5. Keep this pull request draft until the prior Phase B PR is merged and the
   Phase C theorem audit / statement review are independently accepted.
6. Do not claim that any formal theorem empirically validates a cyber-risk
   measurement or a particular calibration profile.

After the branch is checked out on a Windows workstation, run:

```powershell
.\scripts\capture_phase_c.ps1
```

If `lake build` fails, collect and resolve the first actual compiler errors
without weakening the proposition or changing the governing equations.
