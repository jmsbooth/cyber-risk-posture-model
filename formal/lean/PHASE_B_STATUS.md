# Phase B proof status — local machine-check pass; evidence upload pending

Protocol: [CRPI-FVP-001](../../docs/FORMAL_VERIFICATION_PROTOCOL.md)  
Based on accepted [Phase A](PROOF_STATUS.md), Lean 4.24.0 and Mathlib4 commit `f897ebcf72cd16f89ab4577d0c826cd14afaafc7`.  
**Status: LOCAL BUILD AND AXIOM AUDIT PASSED; REVIEW PASSED; NOT YET RELEASE-QUALIFIED.** The repository owner reported the first pinned-toolchain pass for source `e457153dc5ac5b48b432b3a6fec57d492432b1bb`: `lake build` finished successfully (7,358 jobs), and `scripts/capture_phase_b.ps1` reported all 24 theorems and permitted foundational axioms. [Theorem-to-manuscript correspondence](PHASE_B_STATEMENT_REVIEW.md) was independently reviewed and passed. The owner-local generated evidence must still be committed and inspected before changing statuses to **Verified**.

## Scope

| Claim | Module | Candidate mathematical coverage | Status |
| --- | --- | --- | --- |
| P1 | `CRPI/Aggregation.lean` | Finite normalized weighted product equals the manuscript's regularized geometric form | Local pass reported; evidence upload pending |
| P1 | `CRPI/Aggregation.lean` | Bounds in [0,1], all-zero and all-one endpoints | Local pass reported; evidence upload pending |
| P1 | `CRPI/Aggregation.lean` | Zero-weight irrelevance and weak componentwise monotonicity | Local pass reported; evidence upload pending |
| P1 | `CRPI/Aggregation.lean` | Strict increase when some positive-weight input strictly improves | Local pass reported; evidence upload pending |
| P1 | `CRPI/Aggregation.lean` | Nonabsorbing zero when any positively weighted component is positive | Local pass reported; evidence upload pending |
| P1 / consequence mapping | `CRPI/Aggregation.lean` | Domain resilience projection `R_j` bounded, assuming normalized weights and bounded primitives | Local pass reported; evidence upload pending |
| P5 | `CRPI/Direction.lean` | Effective-consequence monotonicity in `D_j`, antitonicity in `R_j` | Local pass reported; evidence upload pending |
| P5 | `CRPI/Direction.lean` | Hazard and effective mitigation directional lemmas | Local pass reported; evidence upload pending |
| P5 | `CRPI/Direction.lean` | Composed instantaneous residual direction in TE, domain consequence, domain resilience, USOM and CM, other variables fixed | Local pass reported; evidence upload pending |

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

The collector reported a successful local run for `e457153...` on 2026-10-22. Two unused-variable warnings from `CRPI/Aggregation.lean` are nonblocking; do not edit mathematical source without re-running the Lean proof acceptance gates.

**Next acceptance action:** Commit the already generated `verification/evidence/e457153dc5ac5b48b432b3a6fec57d492432b1bb/` files from the Windows workspace, push them to PR #2, and inspect their summary and logs. The correspondence review has passed and is [recorded here](PHASE_B_STATEMENT_REVIEW.md). Documentation-only changes since the checked SHA may be accepted under the protocol's scoped evidence rule; theorem source and pinned dependencies must remain byte-for-byte unchanged.

No new machine-check pass is claimed for later mathematical revisions.
