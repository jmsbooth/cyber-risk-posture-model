# CRPI formal proof ledger

Protocol: [CRPI-FVP-001](../../docs/FORMAL_VERIFICATION_PROTOCOL.md)  
Milestone: Phase A — candidate elementary formalization  
Reference baseline: `913c0fe5ffd7950c350383c30eea065416bf544a`  
**Current disposition: LOCAL BUILD AND AXIOM AUDIT REPORTED PASS; RELEASE EVIDENCE PENDING.**
The repository owner supplied successful `lake build` and `#print axioms` output on
2026-10-22. However, the regenerated Lake manifest, exact local source revision,
and reproducible audit evidence have not yet been committed. Treat theorem statuses
as provisionally machine-checked, not release-qualified, until this traceability
and the source-to-manuscript statement review are complete.

| Paper claim / element | Candidate Lean theorem | Hypotheses | Current status |
| --- | --- | --- | --- |
| Common score bounds | `CRPI.bounded_complement`, `CRPI.bounded_mul` | Inputs in [0,1] | Local build/audit reported pass; evidence and statement review pending |
| Normalized weighted sums | `CRPI.weightedSum_bounded` | Finite index, nonnegative weights summing to 1, bounded inputs | Local build/audit reported pass; evidence and statement review pending |
| P2 — CS | `CRPI.consequenceSeverity_bounded` | Same as weighted sums | Local build/audit reported pass; evidence and statement review pending |
| P2 — domain consequence | `CRPI.effectiveConsequence_bounded` | Bounded D, R, rho; normalized v | Local build/audit reported pass; evidence and statement review pending |
| P2 — hazard | `CRPI.hazard_bounded` | Bounded TE and D_eff | Local build/audit reported pass; evidence and statement review pending |
| P2 — mitigation | `CRPI.mitigation_bounded` | Bounded USOM, CM, m0 | Local build/audit reported pass; evidence and statement review pending |
| P2 — instantaneous residual | `CRPI.instantaneousResidual_bounded` | Bounded H and M | Local build/audit reported pass; evidence and statement review pending |
| P6 — envelope | `CRPI.envelope_bounded` | Bounded R_inst and stock | Local build/audit reported pass; evidence and statement review pending |
| P6 — monotonic envelope | `CRPI.envelope_mono_residual`, `CRPI.envelope_mono_stock` | Componentwise order | Local build/audit reported pass; evidence and statement review pending |
| P1 — regularized geometric aggregation | No declaration in Phase A | Positive epsilon, normalized nonnegative weights | Planned Phase B |
| P3/P4 — persistence and cadence | No declaration in Phase A | Fixed interval inputs, nonnegative rates | Planned Phase C |
| P5 — directional sensitivity | No declaration in Phase A | Hold other inputs fixed | Planned Phase B |

### Trust and execution audit

- Toolchain requested: Lean v4.24.0 / Mathlib4 v4.24.0.
- Toolchain execution: **Owner reports success** on Windows with Lean v4.24.0; independent tool versions still require capture.
- Package acquisition: **Owner reports `lake update` and cache retrieval succeeded**; lockfile regeneration requires review and commit.
- `lake build`: **Owner-reported pass**, 7,356 jobs.
- `lake env lean CRPI/Audit.lean`: **Owner-reported pass**, all 11 listed theorem declarations.
- Parser/type-check/kernel result: **Owner-reported successful Lean compilation**; exact-revision evidence pending.
- Foundational axiom output: **Owner-reported `propext`, `Classical.choice`, `Quot.sound` only** for all 11 theorems; these are ordinary foundational Lean/Mathlib axioms. Archive full logs before release.
- Python reference-vector conformance: **Not part of Phase A; pending Phase D**.
- The protocol does not permit a successful theorem label based solely on
  source inspection or on passing Python checks.

### Promotion gate

Before declaring Phase A complete: reconcile and commit the generated Lake
manifest; run `scripts/capture_phase_a.ps1` after committing the lockfile;
review the theorem statements against the manuscript (not just theorem names);
commit the exact-revision evidence; and confirm the release gate against the
recorded proof audit. Only then change corresponding statuses to **Verified**.

**No theorem has been promoted to release-qualified Verified. No CRPI v0.1 formal-spec tag is authorized.**
