# CRPI Phase D — Independent Numerical Conformance

**Protocol:** [CRPI-FVP-001](../docs/FORMAL_VERIFICATION_PROTOCOL.md)  
**Status: NUMERICAL CONFORMANCE VERIFIED — owner-local test evidence accepted for the exact source revision. Manuscript PDF build remains untested.**  
**Baseline:** [Phase A](../formal/lean/PROOF_STATUS.md) (11), [Phase B](../formal/lean/PHASE_B_STATUS.md) (24), and [Phase C](../formal/lean/PHASE_C_STATUS.md) (21) conditional Lean theorem declarations were already machine-checked and merged. Phase D is a separate numerical check, not a new proof of real-number equations.

## Source hierarchy and numerical oracle

The paper's [Governing Model](../paper/CRM_revised.tex) is the authority for all functional forms. The production-independent [Decimal oracle](../scripts/regenerate_phase_d.py) uses Python standard-library Decimal at **70-digit precision** and *does not import the float reference module*. It independently evaluates the exact manuscript expressions for the regularized geometric operator, domain-adjusted consequences, hazard, mitigation, instantaneous residual and the constant-input exact exponential stock transition.

[reference_vectors.json](reference_vectors.json) freezes the input and expected-value pairs as decimal strings, rounded to 32 places after high-precision evaluation. Its covered data consist of:

| Surface | Fixed vectors | Coverage |
| --- | ---: | --- |
| Finite regularized geometric operator and resilience projections | 10 | Manuscript TE example, both endpoints, nonabsorbing zero, zero weight, three components, small, large and near-one epsilon |
| Fully decomposed manuscript example | 1 | TE, CS, domain-specific D_eff, H, M, R_inst, q, stock equilibrium, S_next, CRPI |
| Exact stock-flow transition | 8 | Both ways to reach q=0, dt=0, approach from above/below, nominal update, stock at 1, long-interval accumulation |
| Published synthetic scenarios | 5 | README's initial, peak, final CRPI and coverage qualification, compared as **rounded display values** |
| Additional deterministic seeded cases | 120 | Float weighted geometric outputs compared to independent high-precision oracle across 3-coordinate inputs |

### Declared tolerances

- Core numeric values: `abs_tol = 5e-11`, `rel_tol = 5e-11`, compared to the full-precision oracle's fixed decimal values.
- Manuscript walkthrough and README scenario **display-only** rounded numbers: absolute tolerance `0.0015`. This does not relax comparison to the frozen exact numerical vectors.
- All-zero and all-one endpoints are explicitly tested. The test suite checks that scalar RRAS remains a *reporting aggregate*, never an accidental extra multiplicative hazard or consequence factor.
- All fields under `worked_example.inputs.domain_resilience` are the paper's approximate displayed R_j projection values; this vector is **not** misrepresented as an unrounded source-primitives reconstruction.

The vectors are a declared **float-versus-real conformance test**, not an attempt to prove Python floating-point semantics with Lean. Extreme floating-point regimes beyond the tested epsilon/rate ranges remain a documented boundary of numerical assurance.

## Implementation boundary findings and repairs

Phase D inspection found three numerical-contract defects, classified as **finite-precision implementation limitations**, not incorrect governing equations:

1. `models.crm_reference._validate_weights` previously tolerated weight sums deviating from one by as much as `1e-9`; this exceeded the implementation's `1e-12` bounded-output roundoff clamp and could allow aggregate values above 1. It now rejects weight sums deviating by more than `1e-12`, while preserving valid profile weights with machine-precision rounding.
2. `models.crm_reference.update_persistent_stock` validated beta and kappa individually as finite, but their sum-of-products `q` could overflow to infinity, making `beta * residual / q` silently return an incorrect equilibrium. It now explicitly rejects a nonfinite `q` instead of returning a misleading state.

3. `regularized_geometric` previously computed `(exp(L)-epsilon)/(1-epsilon)` directly for any `epsilon<1`. For `epsilon` extremely close to 1, subtractive cancellation could produce an incorrect value (for example, 1 instead of approximately 0.55). The implementation now uses the **exact real-arithmetic identity** `1 + expm1(L)/(1-epsilon)` for `epsilon>0.5`, calculating each log term as `log1p(-(1-epsilon)*(1-x_i))`; at smaller epsilon the existing log-product path is retained. A near-one epsilon fixed golden vector is included.

The formulas for `G_epsilon`, `D_eff`, `H`, `M`, `R_inst`, the exact exponential update and `max` were **not changed**. Only float evaluation stability and input guards were adjusted. No model recalibration, new construct, or semantic scope extension is introduced.

## Reproducible execution

To reproduce the accepted tests on a clean local checkout with Python 3.10+ and the **pinned** Lean 4.24.0/Lake/Mathlib4 dependencies:

```powershell
python scripts/regenerate_phase_d.py --check
python -m unittest discover -v
python scripts/validate_model.py
python scripts/run_scenarios.py
python scripts/capture_phase_d.py
```

The last command reruns the earlier checks, rebuilds the full Lean target and audits **all 56 theorem declarations**, checks the pinned compiler and Mathlib, and creates `verification/evidence/<source-sha>/phase-d-*` logs and an exact-source JSON summary. For an optional manuscript PDF build add `--with-tex` (requires Tectonic); it explicitly records whether that check was run.

Run evidence capture **only with committed source changes**; no working-tree edits to the manuscript, models, tests, vectors, calibration, scripts, or Lean sources are permitted. Commit and push the resulting small, non-sensitive evidence directory to this PR.

## Accepted machine-check and numerical evidence (2026-10-22)

The repository owner ran `python scripts/capture_phase_d.py` from source revision **`509c5ae448cddbcd062ad8c984c713d73c07c345`**, then committed the [complete ten-file evidence archive](evidence/509c5ae448cddbcd062ad8c984c713d73c07c345/phase-d-summary.json) in `f6f052eea91007a3ea312b082426bde0db490dd9`. Each log and the JSON attestation were fetched independently from GitHub and reviewed. GitHub comparison from tested source to the evidence commit showed **only generated evidence files**; no mathematical code, test logic, vectors, manuscript equations, dependency pins, or calibration inputs changed.

| Acceptance check | Recorded result |
| --- | --- |
| Python runtime | **3.11.15**, Windows |
| Independent 70-digit Decimal oracle | **PASS**, 44 expected-value fields |
| Python unit and conformance tests | **PASS**, 19/19; [test log](evidence/509c5ae448cddbcd062ad8c984c713d73c07c345/phase-d-python_unittest.log) |
| Mathematical invariant suite | **PASS**, 5/5 |
| Synthetic scenario runner | **PASS**, 25 rows across 5 scenarios |
| Pinned Lean/Mathlib build | **PASS**, 7,359 jobs, nonblocking Phase B unused-hypothesis warnings |
| Axiom audits | **PASS**, Phase A 11/11, Phase B 24/24, Phase C 21/21 |
| Trusted axioms | Only `propext`, `Classical.choice`, `Quot.sound` |
| Manifest and toolchain | `leanprover/lean4:v4.24.0` and Mathlib `f897ebcf72cd16f89ab4577d0c826cd14afaafc7`; manifest SHA-256 `c3c1ac12354571388bf36c1532f77dfe9ffa7cac846f786b479b3c072d10e308` |
| Manuscript PDF regeneration | **NOT RUN**, explicitly recorded as `--with-tex not requested` |

**Tolerance review:** The archived reference vectors declared `abs_tol=rel_tol=5e-11` for core numerical comparisons and `abs_tol=0.0015` for deliberately rounded manuscript/README display figures. This is a finite synthetic conformance claim, **not** an all-input IEEE floating-point proof. The corpus includes the near-`epsilon=1` condition and the negative-input cases for the three numerical-contract repairs.

## Final acceptance and publication boundary

- [x] High-precision independent oracle and 44 expected-value fields regenerated and checked.
- [x] Python conformance tests, including exact stock state transitions, numerical boundaries and calibration-profile scenarios, executed on the reference model and passed.
- [x] Previous Phase A–C mathematical declarations replayed and audited under the pinned toolchain.
- [x] Source-match check and complete machine-verification evidence archived under Git.
- [x] All six propositions mapped to their required machine-checked mathematical counterparts in the [verification coverage matrix](PROOF_COVERAGE_MATRIX.md).
- [x] Phase D numerical conformance technical gate accepted.
- [ ] Manuscript's final publication PDF rebuilt, inspected, and linked from the repository. This is a **separate publication-artifact gate**; it is not represented as passing in the Phase D summary.
- [ ] Broader empirical testing/calibration on organizational data, which is outside the bounded formal-verification milestone.

**Decision:** Phase D may merge into `main` under the local-manual evidence policy. The **bounded mathematical-verification and Python numerical-conformance milestone is complete** in its stated conditions. Do not claim that CRPI predictions are empirically validated, that general time-varying ODE solutions were formally proved, or that the final manuscript PDF was publication-tested. No comprehensive paper-release tag or publication-ready PDF claim is authorized by this evidence alone. The optional Proposition 6 nondifferentiability statement remains analytically argued rather than independently Lean-checked.
