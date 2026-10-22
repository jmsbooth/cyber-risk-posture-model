# CRPI Phase A — Theorem-to-Manuscript Correspondence Review

**Date:** 2026-10-22  
**Protocol:** [CRPI-FVP-001](../../docs/FORMAL_VERIFICATION_PROTOCOL.md)  
**Review basis:** CRPI manuscript on `main` (`paper/CRM_revised.tex`, Governing Model and Analytical Properties), and the Phase A definitions under `formal/lean/CRPI/`.  
**Disposition:** **PASS for Phase A statement correspondence**, with expressly limited scope below. Machine-check acceptance is documented by the [Lean 4.24.0 source-revision evidence](../../verification/evidence/b50dea4aaf40cad56c42cff436d450278459efbf/summary.json), captured for source `b50dea4aaf40cad56c42cff436d450278459efbf` and committed at `962f05a674dfc2a58ca9d8e0f1ed15268e4ba891`.

## Mathematical correspondence

| Manuscript construct / property | Formalization and theorem | Statement review |
| --- | --- | --- |
| All scores in `[0,1]` | `Bounded x := 0 ≤ x ∧ x ≤ 1` in `CRPI/Basic.lean` | **Matches.** This is a hypothesis for primitive input scores, not a proof that the data source provides valid scores. |
| Bounds for product / complement | `bounded_mul`, `bounded_complement` | **Matches.** Used as auxiliary lemmas; no hidden calibration assumptions. |
| Normalized weighted sums | `weightedSum` / `weightedSum_bounded` | **Matches.** Finite domain, weights `≥0` with sum 1, bounded operands; the same condition stated for consequence composition in the manuscript. |
| Consequence Severity reporting score, `CS=Σ v_j D_j` | `consequenceSeverity` / `consequenceSeverity_bounded` | **Matches.** Independent reporting aggregate; no scalar RRAS factor is inserted. |
| Adjusted consequence, `D_eff=Σ v_j D_j (1−rho_j R_j)` | `effectiveConsequence` / `effectiveConsequence_bounded` | **Matches.** Depends explicitly on bounded domain-specific `R_j` values, bounded mitigability, and normalized consequence weights. It does **not** prove the resilience projection formula or construct validity. |
| Hazard, `H=TE × D_eff` | `hazard` / `hazard_bounded` | **Matches.** Requires bounded `TE` and `D_eff`. |
| Mitigation, `M=USOM × [m0+(1−m0)CM]` | `mitigation` / `mitigation_bounded` | **Matches.** Argument order is explicit; no alternative prevention/remediation term was introduced. |
| Instantaneous residual, `R_inst=H(1−M)` | `instantaneousResidual` / `instantaneousResidual_bounded` | **Matches.** Requires bounded hazard and mitigation. |
| Envelope, `CRPI=max(R_inst,S)` | `envelope` / `envelope_bounded` | **Matches.** Proposition 6 explicitly assumes bounded residual and stock; the proof correctly does not pretend to establish persistence invariance. |
| Envelope coordinate monotonicity | `envelope_mono_residual` and `envelope_mono_stock` | **Matches.** Each proof fixes the other argument. The non-differentiability statement in Proposition 6 is optional under the protocol and not formalized here. |

## Boundary of this review

1. **Conditional versus end-to-end boundedness:** `R_j` is treated as an already bounded domain resilience projection. Proving its regularized geometric construction, `TE` aggregation, and associated endpoints/monotonicity belongs to **Phase B**.
2. **Persistent stock is an input here:** No stock-flow state update, equilibrium, or cadence theorem is part of Phase A. The conditional `CRPI` bound therefore does not claim to prove an end-to-end bounded state trajectory. Persistence belongs to **Phase C**.
3. **No general empirical statement follows:** The proof hypotheses concern real-valued inputs and governed coefficients. They do not show measurements, parameters, impact domains, or cyber-risk phenomena have been validated.
4. **No false completeness claim:** The 11 Phase A declarations cover supporting lemmas and the boundedness parts of Propositions 2 and 6, not all six analytical propositions in the paper.
5. **Compiler attestation reconciled:** The initial collector reported root-selected Lean 4.35.0, rather than the effective compiler inside the project. The corrected collector enforces and records **Lean 4.24.0** inside `formal/lean`; the evidence and axiom audit passed for source `b50dea4`. Both records are retained, and the corrected one supersedes the original for acceptance.

## Acceptance and next action

The source-to-manuscript comparison for the Phase A statements is approved
**within the above assumptions and scope**, and the toolchain-attested
machine-check evidence is committed. The ledger may therefore label these
**specific conditional theorem statements** Verified. This acceptance supports
merging Phase A. It does **not** verify the entire manuscript, all six
propositions, or the empirical validity of CRPI.
