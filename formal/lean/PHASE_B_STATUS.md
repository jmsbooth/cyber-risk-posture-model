# Phase B proof status — candidate, unverified

Protocol: [CRPI-FVP-001](../../docs/FORMAL_VERIFICATION_PROTOCOL.md)  
Based on accepted [Phase A](PROOF_STATUS.md), Lean 4.24.0 and Mathlib4 commit `f897ebcf72cd16f89ab4577d0c826cd14afaafc7`.  
**Status: PREPARED ONLY. No Phase B `lake build`, axiom audit, or machine-check evidence has run.**

## Scope

| Claim | Module | Candidate mathematical coverage | Status |
| --- | --- | --- | --- |
| P1 | `CRPI/Aggregation.lean` | Finite normalized weighted product equals the manuscript's regularized geometric form | Candidate, build pending |
| P1 | `CRPI/Aggregation.lean` | Bounds in [0,1], all-zero and all-one endpoints | Candidate, build pending |
| P1 | `CRPI/Aggregation.lean` | Zero-weight irrelevance and weak componentwise monotonicity | Candidate, build pending |
| P1 | `CRPI/Aggregation.lean` | Strict increase when some positive-weight input strictly improves | Candidate, build pending |
| P1 | `CRPI/Aggregation.lean` | Nonabsorbing zero when any positively weighted component is positive | Candidate, build pending |
| P1 / consequence mapping | `CRPI/Aggregation.lean` | Domain resilience projection `R_j` bounded, assuming normalized weights and bounded primitives | Candidate, build pending |
| P5 | `CRPI/Direction.lean` | Effective-consequence monotonicity in `D_j`, antitonicity in `R_j` | Candidate, build pending |
| P5 | `CRPI/Direction.lean` | Hazard and effective mitigation directional lemmas | Candidate, build pending |
| P5 | `CRPI/Direction.lean` | Composed instantaneous residual direction in TE, domain consequence, domain resilience, USOM and CM, other variables fixed | Candidate, build pending |

There are **24 declared audit targets** in `CRPI/AuditB.lean`. Unlike the Phase A conditional envelope result, P5 speaks about the full **composed instantaneous residual**, not an ad hoc proxy. No theorem asserts a result about historical stock or financial loss.

## Acceptance gates

1. The current proof branch must build using the pinned Lean 4.24.0 and unchanged Mathlib revision, not the root-selected elan default.
2. All 24 declarations must exist, be accepted by Lean's kernel and appear in `#print axioms`.
3. No `sorry`, `admit`, custom `axiom`, `unsafe` proof dependency or `native_decide`.
4. Check all theorem hypotheses and exact mathematical statements against Proposition 1, Proposition 5, and the Governing Model.
5. Commit an exact-revision `verification/evidence/<source-commit>/` record; log unexpected axioms as a blocker.
6. Merge Phase B independently of Phase C when qualified. Keep the manuscript's blanket verification claims unchanged until the whole protocol is satisfied.

Run from a clean Windows repository root after the sources are committed:

```powershell
.\scripts\capture_phase_b.ps1
```

The collector records evidence **only if** the build and theorem audit succeed. Compilation errors are work to fix; they are not grounds to weaken the governing equations.
