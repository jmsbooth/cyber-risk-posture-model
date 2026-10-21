# CRPI Lean 4 formalization — Phase A

This is the initial *unverified working formalization* of the elementary
mathematical CRPI equations. It follows
[CRPI-FVP-001](../../docs/FORMAL_VERIFICATION_PROTOCOL.md).

**Status: candidate sources, not machine-checked.** The authoring environment did
not have Lean/Lake installed and could not reach a package host. No successful
Lean build, axiom audit, or formal theorem acceptance is asserted.

## Frozen dependency versions

- Lean toolchain: `leanprover/lean4:v4.24.0`.
- Mathlib4 tag: `v4.24.0`.
- Mathlib4 exact source revision: `f897ebcf72cd16f89ab4577d0c826cd14afaafc7`.
- The included `lake-manifest.json` is **derived from the matching upstream
  Mathlib release lock** and must be reconciled using Lake, then independently
  reviewed before it is called a validated dependency lock. No version upgrade
  is authorized by this operation.

Mathlib's v4.24.0 `lean-toolchain` explicitly selects Lean v4.24.0.

## Local execution

From the repository root, with git, elan, and a network-capable setup for the
first dependency fetch:

```bash
cd formal/lean
lake update
lake exe cache get
lake build
lake env lean CRPI/Audit.lean
```

If `lake update` changes the lockfile, review the difference against the
recorded pins before accepting it. A successful cache retrieval alone does
not establish a successful build. Local test results must be captured against
the exact source revision.

## Current proof coverage

- `CRPI.Basic`: real-interval complements and products; bounded finite
  normalized weighted sums.
- `CRPI.Consequence`: reporting consequence aggregate, resilience-adjusted
  consequence, and hazard boundedness.
- `CRPI.Mitigation`: effective mitigation and instantaneous residual bounds.
- `CRPI.Envelope`: CRPI envelope boundedness and coordinate monotonicity.

These are **candidate Lean declarations**. See
[PROOF_STATUS.md](PROOF_STATUS.md) for the proof/assumption ledger.
Formal aggregation using the regularized geometric operator belongs to
Phase B; exact stock-flow transition to Phase C.

Do not describe the paper as formally verified on the basis of these files.
The manuscript's existing analytical appendix remains analytical, not a
machine-checked result, until the acceptance gates are satisfied.
