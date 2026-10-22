# Phase B proof status — Verified, conditional Proposition 1 and 5 properties

Protocol: [CRPI-FVP-001](../../docs/FORMAL_VERIFICATION_PROTOCOL.md)  
Based on accepted [Phase A](PROOF_STATUS.md), Lean 4.24.0 and Mathlib4 commit `f897ebcf72cd16f89ab4577d0c826cd14afaafc7`.  
**Status: PHASE B VERIFIED — within the stated mathematical hypotheses and scope.** The [exact-revision evidence](../../verification/evidence/e457153dc5ac5b48b432b3a6fec57d492432b1bb/phase-b-summary.json) was published on the Phase B branch, and the repository-hosted build and 24-declaration axiom logs were inspected. Lean 4.24.0 and pinned Mathlib revision `f897ebcf72cd16f89ab4577d0c826cd14afaafc7` were attested; build and axiom audit exit codes were both zero. The [theorem-to-manuscript correspondence](PHASE_B_STATEMENT_REVIEW.md) passed. **The accepted evidence applies to source `e457153dc5ac5b48b432b3a6fec57d492432b1bb`; later changes were documentation/evidence-only.**

## Scope

| Claim | Module | Candidate mathematical coverage | Status |
| --- | --- | --- | --- |
| P1 | `CRPI/Aggregation.lean` | Finite normalized weighted product equals the manuscript's regularized geometric form | **Verified (Phase B; conditional)** |
| P1 | `CRPI/Aggregation.lean` | Bounds in [0,1], all-zero and all-one endpoints | **Verified (Phase B; conditional)** |
| P1 | `CRPI/Aggregation.lean` | Zero-weight irrelevance and weak componentwise monotonicity | **Verified (Phase B; conditional)** |
| P1 | `CRPI/Aggregation.lean` | Strict increase when some positive-weight input strictly improves | **Verified (Phase B; conditional)** |
| P1 | `CRPI/Aggregation.lean` | Nonabsorbing zero when any positively weighted component is positive | **Verified (Phase B; conditional)** |
| P1 / consequence mapping | `CRPI/Aggregation.lean` | Domain resilience projection `R_j` bounded, assuming normalized weights and bounded primitives | **Verified (Phase B; conditional)** |
| P5 | `CRPI/Direction.lean` | Effective-consequence monotonicity in `D_j`, antitonicity in `R_j` | **Verified (Phase B; conditional)** |
| P5 | `CRPI/Direction.lean` | Hazard and effective mitigation directional lemmas | **Verified (Phase B; conditional)** |
| P5 | `CRPI/Direction.lean` | Composed instantaneous residual direction in TE, domain consequence, domain resilience, USOM and CM, other variables fixed | **Verified (Phase B; conditional)** |

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

**Final acceptance record:** Phase B machine-check source revision `e457153dc5ac5b48b432b3a6fec57d492432b1bb` is preserved in the [Windows build and axiom archive](../../verification/evidence/e457153dc5ac5b48b432b3a6fec57d492432b1bb/phase-b-summary.json). The archive attests Lean 4.24.0, Lake 5.0.0, pinned Mathlib4, and manifest SHA-256 `c3c1ac12354571388bf36c1532f77dfe9ffa7cac846f786b479b3c072d10e308`. Each of the 24 theorem entries has only foundational axioms `propext`, `Classical.choice`, `Quot.sound`. Two unused-variable linter warnings are nonblocking and recorded in the archived build log.

**Source integrity:** GitHub comparison from `e457153d...` to acceptance head shows only this review/status documentation and the three evidence files. No changes to `CRPI/Aggregation.lean`, `CRPI/Direction.lean`, `CRPI.lean`, `lake-manifest.json`, or the pinned toolchain.

**Release scope:** Phase B covers Proposition 1 geometric bounds, endpoints, zero weight, order behavior, nonabsorbing zero and bounded domain projections; and Proposition 5 non-strict **instantaneous residual** directionality under the declared hypotheses. The paper's derivative identities were not separately formalized. Phase C stock-flow and cadence properties remain separately qualified, and model-level empirical validity is not established.

**Decision:** Phase B is eligible for merge into `main`. No six-proposition release tag is authorized solely from Phases A/B.
