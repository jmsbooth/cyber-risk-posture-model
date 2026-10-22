# CRPI formal proof ledger

Protocol: [CRPI-FVP-001](../../docs/FORMAL_VERIFICATION_PROTOCOL.md)  
Milestone: Phase A — conditional elementary boundedness theorems  
Reference baseline: `913c0fe5ffd7950c350383c30eea065416bf544a`  
**Current disposition: PHASE A VERIFIED — conditional theorem scope only.**
The exact-revision Windows build and 11-theorem axiom audit passed using
**Lean 4.24.0**, the declared project compiler, with the pinned Mathlib revision.
The accepted [Phase A verification evidence](../../verification/evidence/b50dea4aaf40cad56c42cff436d450278459efbf/summary.json)
was captured for mathematical source revision
`b50dea4aaf40cad56c42cff436d450278459efbf` and committed at
`962f05a674dfc2a58ca9d8e0f1ed15268e4ba891`.
The [theorem-to-manuscript correspondence review](PHASE_A_STATEMENT_REVIEW.md)
passed for **the stated conditional mathematical properties**.
Later changes to the evidence ledger and documentation do not alter the
kernel-checked definitions or theorems. The remaining manuscript propositions
are explicitly open for Phases B and C.

| Paper claim / element | Candidate Lean theorem | Hypotheses | Current status |
| --- | --- | --- | --- |
| Common score bounds | `CRPI.bounded_complement`, `CRPI.bounded_mul` | Inputs in [0,1] | **Verified (Phase A; conditional)** |
| Normalized weighted sums | `CRPI.weightedSum_bounded` | Finite index, nonnegative weights summing to 1, bounded inputs | **Verified (Phase A; conditional)** |
| P2 — CS | `CRPI.consequenceSeverity_bounded` | Same as weighted sums | **Verified (Phase A; conditional)** |
| P2 — domain consequence | `CRPI.effectiveConsequence_bounded` | Bounded D, R, rho; normalized v | **Verified (Phase A; conditional)** |
| P2 — hazard | `CRPI.hazard_bounded` | Bounded TE and D_eff | **Verified (Phase A; conditional)** |
| P2 — mitigation | `CRPI.mitigation_bounded` | Bounded USOM, CM, m0 | **Verified (Phase A; conditional)** |
| P2 — instantaneous residual | `CRPI.instantaneousResidual_bounded` | Bounded H and M | **Verified (Phase A; conditional)** |
| P6 — envelope | `CRPI.envelope_bounded` | Bounded R_inst and stock | **Verified (Phase A; conditional)** |
| P6 — monotonic envelope | `CRPI.envelope_mono_residual`, `CRPI.envelope_mono_stock` | Componentwise order | **Verified (Phase A; conditional)** |
| P1 — regularized geometric aggregation | No declaration in Phase A | Positive epsilon, normalized nonnegative weights | Planned Phase B |
| P3/P4 — persistence and cadence | No declaration in Phase A | Fixed interval inputs, nonnegative rates | Planned Phase C |
| P5 — directional sensitivity | No declaration in Phase A | Hold other inputs fixed | Planned Phase B |

### Trust and execution audit

- Declared project toolchain: `leanprover/lean4:v4.24.0`; Mathlib4 pinned to `f897ebcf72cd16f89ab4577d0c826cd14afaafc7`.
- Lake-resolved lockfile: **committed** at `c75d07309581454e01fb4ef9eba120a720423d4d`.
- Archived source-revision build: **PASS**, 7,356 jobs, exit code 0.
- Archived theorem axiom audit: **PASS**, 11 declarations, exit code 0.
- Foundational axioms: `propext`, `Classical.choice`, and `Quot.sound` only; all are standard permitted axioms.
- Effective project compiler: **Lean 4.24.0**, `797c613eb9b6d4ec95db23e3e00af9ac6657f24b`; Lake `5.0.0-src+797c613`. The collector ran its version probe inside `formal/lean` and enforced the repository pin.
- Earlier root-level Lean 4.35.0 evidence was superseded by the verified project-specific attestation; the historical artifact remains retained for provenance.
- Attested build source SHA: `b50dea4aaf40cad56c42cff436d450278459efbf`.
- Axiom audit: each of the 11 theorem statements depends only on the permitted foundational axioms `propext`, `Classical.choice`, `Quot.sound`.
- Theorem-to-manuscript comparison: **PASS for Phase A conditional claims** — [review](PHASE_A_STATEMENT_REVIEW.md).
- End-to-end Tier 2 geometric bounds, stock-flow evolution, and directional behavior: **not yet formalized** (Phases B/C).
- Python reference-vector conformance: **not part of Phase A; pending Phase D**.
- Source inspection and reported build results are not treated as evidence of empirical validity.

### Promotion gate

**Phase A accepted:** the 11 named theorems are Lean machine-checked, their
hypotheses and correspondence were reviewed, and exact-revision evidence was
committed. The evidence record shows zero build/audit exit codes and includes the
pinned compiler, Mathlib revision, SHA-256 of the resolved manifest, and permitted
axioms. No mathematical Lean source changed between evidence capture and this
ledger update; only evidence and documentation were amended.

**Strict limits:** Phase A does not prove the geometric aggregation operator (P1),
the stock-flow transition and cadence consistency (P3/P4), directional sensitivity
(P5), or the non-differentiability subclaim of P6. Proposition 6's envelope
boundedness is proved **conditional on bounded persistent stock**; proving
that stock remains bounded belongs to Phase C.

**Release decision:** Phase A may merge into `main`. Do **not** publish a
full CRPI v0.1 formal-spec tag or a blanket claim that all six propositions are
machine-checked. Those claims require subsequent proof phases and the protocol's
full conformance gates.
