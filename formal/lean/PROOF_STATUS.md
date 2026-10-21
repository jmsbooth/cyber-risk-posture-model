# CRPI formal proof ledger

Protocol: [CRPI-FVP-001](../../docs/FORMAL_VERIFICATION_PROTOCOL.md)  
Milestone: Phase A — candidate elementary formalization  
Reference baseline: `913c0fe5ffd7950c350383c30eea065416bf544a`  
**Current disposition: NOT VERIFIED.** All declarations below require a real
`lake build` and axiom audit under the pinned dependencies.

| Paper claim / element | Candidate Lean theorem | Hypotheses | Current status |
| --- | --- | --- | --- |
| Common score bounds | `CRPI.bounded_complement`, `CRPI.bounded_mul` | Inputs in [0,1] | Prepared; build not run |
| Normalized weighted sums | `CRPI.weightedSum_bounded` | Finite index, nonnegative weights summing to 1, bounded inputs | Prepared; build not run |
| P2 — CS | `CRPI.consequenceSeverity_bounded` | Same as weighted sums | Prepared; build not run |
| P2 — domain consequence | `CRPI.effectiveConsequence_bounded` | Bounded D, R, rho; normalized v | Prepared; build not run |
| P2 — hazard | `CRPI.hazard_bounded` | Bounded TE and D_eff | Prepared; build not run |
| P2 — mitigation | `CRPI.mitigation_bounded` | Bounded USOM, CM, m0 | Prepared; build not run |
| P2 — instantaneous residual | `CRPI.instantaneousResidual_bounded` | Bounded H and M | Prepared; build not run |
| P6 — envelope | `CRPI.envelope_bounded` | Bounded R_inst and stock | Prepared; build not run |
| P6 — monotonic envelope | `CRPI.envelope_mono_residual`, `CRPI.envelope_mono_stock` | Componentwise order | Prepared; build not run |
| P1 — regularized geometric aggregation | No declaration in Phase A | Positive epsilon, normalized nonnegative weights | Planned Phase B |
| P3/P4 — persistence and cadence | No declaration in Phase A | Fixed interval inputs, nonnegative rates | Planned Phase C |
| P5 — directional sensitivity | No declaration in Phase A | Hold other inputs fixed | Planned Phase B |

### Trust and execution audit

- Toolchain requested: Lean v4.24.0 / Mathlib4 v4.24.0.
- Toolchain execution: **Not run** — no Lean/Lake binary in the execution environment.
- Package acquisition: **Not run** — outbound GitHub DNS/network unavailable
  from the execution environment.
- `lake build`: **Not run**.
- `lake env lean CRPI/Audit.lean`: **Not run**.
- Parser/type-check/kernel result: **Unknown**; do not imply these sources compile.
- Third-party foundational axioms: **Not audited**.
- Python reference-vector conformance: **Not part of Phase A; pending Phase D**.
- The protocol does not permit a successful theorem label based solely on
  source inspection or on passing Python checks.

### Promotion gate

Before declaring Phase A complete: install the pinned toolchain, reconcile the
generated Lake manifest, correct any compiler/type errors, run the complete
build and `#print axioms` audit, review theorem statements against the
manuscript (not only theorem names), and commit an exact-revision evidence
record. Only then change corresponding statuses to **Verified**.

**No proof has been promoted. No CRPI v0.1 formal-spec tag is authorized.**
