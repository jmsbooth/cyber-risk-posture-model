# Phase C proof status — local machine-check pass; evidence upload pending

Protocol: [CRPI-FVP-001](../../docs/FORMAL_VERIFICATION_PROTOCOL.md)  
Phase B's [24 conditional proofs are verified and merged](PHASE_B_STATUS.md) in PR #2. The accepted Phase A proofs are unchanged. Phase C PR #3 is now based on `main`.  
**Status: LOCAL LEAN BUILD AND AXIOM AUDIT REPORTED PASS; STATEMENT REVIEW PASSED; ARCHIVED ACCEPTANCE PENDING.** The owner reran Lean 4.24.0 after correcting `intervalStep_tendsto_equilibrium`. From exact source `9dab18ba0e7045c28754746a0ba61a2cb1d2e592`, `lake build` finished successfully (**7,359 jobs**) and `scripts/capture_phase_c.ps1` reported **21 theorem-level axiom audits**, all using only the permitted foundational axioms. The source-to-[manuscript correspondence review](PHASE_C_STATEMENT_REVIEW.md) is complete. The generated Windows files at `verification/evidence/9dab18ba0e7045c28754746a0ba61a2cb1d2e592/` must still be committed to GitHub and inspected before any theorem is labeled release-qualified **Verified**.

## Manuscript alignment and proof scope

| Claim | Candidate Lean theorem | Goal | Status |
| --- | --- | --- | --- |
| P3 | `totalRate_nonneg` / `zero_totalRate_zero_terms` | Nonnegative rates and degenerate no-update case | Local pass reported; evidence archive pending |
| P3 | `stockDrift_affine`, `stockDrift_lower_boundary_nonneg`, `stockDrift_upper_boundary_nonpos`, `stockDrift_zero_iff_equilibrium` | Exact ODE drift, inward boundaries, unique equilibrium when q>0 | Local pass reported; evidence archive pending |
| P3 | `stockEquilibrium_bounded` | Equilibrium in [0,1] when total rate positive | Local pass reported; evidence archive pending |
| P3 | `decayFactor_bounded` | Exponential factor in (0,1] for nonnegative elapsed time and rate | Local pass reported; evidence archive pending |
| P3 | `intervalStep_bounded` | Convex-combination invariant | Local pass reported; evidence archive pending |
| P3 | `stockTransition_zero_rate` / `stockTransition_bounded` | Exact update with q=0 branch preserves state and [0,1] | Local pass reported; evidence archive pending |
| P3 | `intervalStep_equilibrium` / `stockTransition_equilibrium` | Fixed equilibrium under constant inputs | Local pass reported; evidence archive pending |
| P3 | `intervalStep_contraction` | Absolute distance to equilibrium never increases | Local pass reported; evidence archive pending |
| P3 | `intervalStep_decreases_above` / `intervalStep_increases_below` | Directional evolution toward equilibrium for longer intervals | Local pass reported; evidence archive pending |
| P3 | `intervalStep_tendsto_equilibrium` / `stockTransition_tendsto_equilibrium` | Convergence as elapsed time tends to infinity when q>0 | Local pass reported; evidence archive pending |
| P4 | `intervalStep_semigroup` / `stockTransition_semigroup` | Exact cadence consistency with identical interval rates and inputs | Local pass reported; evidence archive pending |
| P6 complement | `envelope_after_transition_bounded` | CRPI envelope boundedness using verified P3 stock invariance | Local pass reported; evidence archive pending |

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
2. All **21 Phase C declarations** are checked and appear in
   `lake env lean CRPI/AuditC.lean` without unexpected axioms.
3. The theorem-to-manuscript review [is complete](PHASE_C_STATEMENT_REVIEW.md) for the intended candidate statements; verify that final compiler-accepted declarations retain those statements and assumptions.
4. Commit exact-revision `verification/evidence/<commit>/` proof and axiom logs.
5. The Phase B PR is merged and the source-to-paper review is complete.
   Keep this PR draft until Phase C's exact-revision machine-check artifacts
   are committed and independently accepted.
6. Do not claim that any formal theorem empirically validates a cyber-risk
   measurement or a particular calibration profile.

After the branch is checked out on a Windows workstation, run:

```powershell
.\scripts\capture_phase_c.ps1
```

The owner already ran the collector successfully for source `9dab18ba...`.
**Next step:** commit and push the generated `verification/evidence/9dab18ba0e7045c28754746a0ba61a2cb1d2e592/` directory, then inspect `phase-c-summary.json`, `phase-c-lake-build.log` and `phase-c-axiom-audit.log` against the accepted statements, pinned toolchain and exact source SHA. No source changes are authorized just to remove Phase B's two harmless linter warnings.

Only after the evidence gate passes should this ledger's conditional Phase C statements be promoted to **Verified** and PR #3 merged. The full manuscript is not thereby empirically validated.
