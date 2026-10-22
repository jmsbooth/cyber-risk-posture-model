# CRPI Proposition Verification Matrix

**Date:** 2026-10-22  
**Protocol:** [CRPI-FVP-001](../docs/FORMAL_VERIFICATION_PROTOCOL.md)  
**Authority:** [Manuscript appendix](../paper/CRM_revised.tex), the exact Lean theorem statements and assumptions, and the archived source-revision evidence.

**Decision:** All **six propositions have machine-checked counterparts for their *required* mathematical subclaims**, within the limits described below. The 56 accepted theorem declarations are supporting results, not 56 independent manuscript propositions. The optional analytic P6 non-differentiability claim, Python floating-point conformance (Phase D) and empirical model validity are distinct and have **not** yet been accepted as fully verified.

| Proposition | Lean status | Verified declaration families | Source-matched evidence | Important boundary |
| --- | --- | --- | --- | --- |
| P1 — Regularized aggregation | **Verified (required claims)** | `CRPI.regularizedBase_bounds`, `regularizedProduct_bounds`, `regularizedGeometric_bounded`, `regularizedGeometric_zero`, `regularizedGeometric_one`, zero-weight irrelevance, weak and strict monotonicity, positive-component result | [Phase B evidence](evidence/e457153dc5ac5b48b432b3a6fec57d492432b1bb/phase-b-summary.json) | Weights nonnegative/sum to one; `0<epsilon<1`; primitive scores bounded. Derivative identity itself not checked. |
| P2 — Consequence, hazard, mitigation | **Verified (required claims)** | `CRPI.weightedSum_bounded`, `consequenceSeverity_bounded`, `effectiveConsequence_bounded`, `hazard_bounded`, `mitigation_bounded`, `instantaneousResidual_bounded`, `domainResilience_bounded` | [Phase A](evidence/b50dea4aaf40cad56c42cff436d450278459efbf/summary.json) · [Phase B](evidence/e457153dc5ac5b48b432b3a6fec57d492432b1bb/phase-b-summary.json) | Boundedness conditional on governed weights, domain values, mitigability and applicable resilience; no empirical weight calibration established. |
| P3 — Persistence invariance and equilibrium | **Verified (piecewise-constant exact-transition scope)** | `CRPI.stockDrift_affine`, `stockDrift_zero_iff_equilibrium`, `stockTransition_zero_rate`, `stockTransition_bounded`, `intervalStep_contraction`, equilibrium and convergence lemmas | [Phase C evidence](evidence/9dab18ba0e7045c28754746a0ba61a2cb1d2e592/phase-c-summary.json) | Initial stock/residual/mitigation bounded; rates and duration nonnegative. Not a general nonautonomous ODE theorem. |
| P4 — Cadence consistency | **Verified (fixed inputs/rates)** | `CRPI.intervalStep_semigroup`, `stockTransition_semigroup` | [Phase C](evidence/9dab18ba0e7045c28754746a0ba61a2cb1d2e592/phase-c-summary.json) | Two consecutive intervals must retain the same `R_inst`, `M`, `beta`, `kappa`. |
| P5 — Directional sensitivity | **Verified (order properties)** | `CRPI.currentResidual_mono_threat`, `currentResidual_mono_domain`, `currentResidual_antitone_resilience`, `currentResidual_antitone_usom`, `currentResidual_antitone_cm` and intermediate monotonicity lemmas | [Phase B](evidence/e457153dc5ac5b48b432b3a6fec57d492432b1bb/phase-b-summary.json) | Other inputs held fixed. Monotonicity is checked via inequalities rather than a separate derivative proof. |
| P6 — CRPI envelope | **Verified (required bound and coordinate monotonicity)** | `CRPI.envelope_bounded`, `envelope_mono_residual`, `envelope_mono_stock`, `envelope_after_transition_bounded` | [Phase A](evidence/b50dea4aaf40cad56c42cff436d450278459efbf/summary.json) · [Phase C](evidence/9dab18ba0e7045c28754746a0ba61a2cb1d2e592/phase-c-summary.json) | Envelope nonsmoothness at switching equality remains an analytically stated, **optional and unformalized** claim. |

## Verification trust facts

- **Lean 4.24.0 / pinned Mathlib** was checked on the mathematical source revisions `b50dea4` (A), `e457153d` (B), `9dab18ba` (C).
- **11 + 24 + 21 = 56** declarations were machine-checked. The theorem-by-theorem axiom audits found only standard permitted `propext`, `Classical.choice`, `Quot.sound`.
- Full mathematical correspondence reviews: [A](../formal/lean/PHASE_A_STATEMENT_REVIEW.md), [B](../formal/lean/PHASE_B_STATEMENT_REVIEW.md), [C](../formal/lean/PHASE_C_STATEMENT_REVIEW.md).
- Numerical vector testing is **not a proof about IEEE floating-point under all possible inputs**. It compares `models/crm_reference.py` to an independently generated high-precision Decimal oracle under explicit tolerance and data-contract policies.

## Remaining release conditions

1. Execute and archive the Phase D [conformance suite](PHASE_D_STATUS.md), reconcile any actual implementation discrepancies, and verify source SHA and test output.
2. Document the manuscript PDF build result and preserve the accepted manuscript/README wording. If no TeX build is performed, do not call the manuscript's PDF release tested.
3. Declare only **selected CRPI mathematical invariants formally verified under stated hypotheses**. Do not imply Lean has proved the cyber-risk measurement semantics, organizational data quality, model calibration, incident prediction, losses, or operational efficacy.
