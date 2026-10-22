# CRPI formal proof ledger

Protocol: [CRPI-FVP-001](../../docs/FORMAL_VERIFICATION_PROTOCOL.md)  
Milestone: Phase A — conditional elementary boundedness theorems  
Reference baseline: `913c0fe5ffd7950c350383c30eea065416bf544a`  
**Current disposition: BUILD/AXIOM EVIDENCE ARCHIVED; PROJECT TOOLCHAIN ATTESTATION PENDING.**
The repository owner captured a passing Windows Lean build and an 11-theorem axiom
audit on the exact source revision `c75d07309581454e01fb4ef9eba120a720423d4d`:
[build/audit evidence](../../verification/evidence/c75d07309581454e01fb4ef9eba120a720423d4d/summary.json).
The [Phase A statement review](PHASE_A_STATEMENT_REVIEW.md) passed for the exact
mathematical statements and hypotheses. The first evidence collector recorded
**root-selected Lean 4.35.0** even though the project pins **Lean 4.24.0**.
Release-qualified status requires an updated exact-revision run that records and
asserts the effective *project-selected* compiler before promoting the theorem claims.

| Paper claim / element | Candidate Lean theorem | Hypotheses | Current status |
| --- | --- | --- | --- |
| Common score bounds | `CRPI.bounded_complement`, `CRPI.bounded_mul` | Inputs in [0,1] | Source build/audit pass; effective-toolchain attestation pending |
| Normalized weighted sums | `CRPI.weightedSum_bounded` | Finite index, nonnegative weights summing to 1, bounded inputs | Source build/audit pass; effective-toolchain attestation pending |
| P2 — CS | `CRPI.consequenceSeverity_bounded` | Same as weighted sums | Source build/audit pass; effective-toolchain attestation pending |
| P2 — domain consequence | `CRPI.effectiveConsequence_bounded` | Bounded D, R, rho; normalized v | Source build/audit pass; effective-toolchain attestation pending |
| P2 — hazard | `CRPI.hazard_bounded` | Bounded TE and D_eff | Source build/audit pass; effective-toolchain attestation pending |
| P2 — mitigation | `CRPI.mitigation_bounded` | Bounded USOM, CM, m0 | Source build/audit pass; effective-toolchain attestation pending |
| P2 — instantaneous residual | `CRPI.instantaneousResidual_bounded` | Bounded H and M | Source build/audit pass; effective-toolchain attestation pending |
| P6 — envelope | `CRPI.envelope_bounded` | Bounded R_inst and stock | Source build/audit pass; effective-toolchain attestation pending |
| P6 — monotonic envelope | `CRPI.envelope_mono_residual`, `CRPI.envelope_mono_stock` | Componentwise order | Source build/audit pass; effective-toolchain attestation pending |
| P1 — regularized geometric aggregation | No declaration in Phase A | Positive epsilon, normalized nonnegative weights | Planned Phase B |
| P3/P4 — persistence and cadence | No declaration in Phase A | Fixed interval inputs, nonnegative rates | Planned Phase C |
| P5 — directional sensitivity | No declaration in Phase A | Hold other inputs fixed | Planned Phase B |

### Trust and execution audit

- Declared project toolchain: `leanprover/lean4:v4.24.0`; Mathlib4 pinned to `f897ebcf72cd16f89ab4577d0c826cd14afaafc7`.
- Lake-resolved lockfile: **committed** at `c75d07309581454e01fb4ef9eba120a720423d4d`.
- Archived source-revision build: **PASS**, 7,356 jobs, exit code 0.
- Archived theorem axiom audit: **PASS**, 11 declarations, exit code 0.
- Foundational axioms: `propext`, `Classical.choice`, and `Quot.sound` only; all are standard permitted axioms.
- Captured Lean version: **4.35.0 at repository root**; pinned **4.24.0 in project**. The previous collector did not distinguish them.
- Effective compiler version: **awaiting capture by the corrected project-level probe**.
- Theorem-to-manuscript comparison: **PASS for Phase A conditional claims** — [review](PHASE_A_STATEMENT_REVIEW.md).
- End-to-end Tier 2 geometric bounds, stock-flow evolution, and directional behavior: **not yet formalized** (Phases B/C).
- Python reference-vector conformance: **not part of Phase A; pending Phase D**.
- Source inspection and reported build results are not treated as evidence of empirical validity.

### Promotion gate

To close Phase A: pull the corrected `scripts/capture_phase_a.ps1`; rerun it
against the current clean source revision so that `lake env lean --version`
is evaluated **inside `formal/lean`**, rejects an unexpected version, and
records the new exact-revision evidence. Commit and push the generated record;
then check both the pinned-toolchain output and the source-to-paper
review before marking the specific conditional theorems **Verified**.

**No theorem has been promoted to release-qualified Verified. No CRPI v0.1 formal-spec tag is authorized.**
