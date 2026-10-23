# Cyber Risk Posture Model

Reproducible research artifact for **A Dynamic, Decomposable Operational Cyber Risk
Posture Index**. The repository pairs the manuscript with a small executable reference
implementation, a versioned calibration profile, synthetic use cases, and mathematical
validation checks.

> **Research status:** mathematically specified and synthetically behavior-checked; not yet
> empirically validated. CRPI is an operational posture index, not a breach probability,
> financial-loss estimate, or security guarantee.

## Start here

- [Read the manuscript source](paper/CRM_revised.tex)
- [Download the compiled CRPI manuscript (PDF)](paper/build/CRM_revised.pdf) — tracked Tectonic 0.17.0 build, SHA-256 verified; [final visual publication QA](https://github.com/jmsbooth/cyber-risk-posture-model/issues/5) remains open
- [Run the reference model](models/crm_reference.py)
- [Inspect the calibration profile](config/calibration_baseline.json)
- [Review the synthetic scenarios](data/examples/scenarios.csv)

## Why this repository exists

Cyber risk changes over time and rarely has one explanatory driver. The paper defines a
bounded, decomposable model that keeps five operational constructs distinct:

| Construct | Meaning | Model role |
| --- | --- | --- |
| CM | Continuous Monitoring | Modulates how effectively operations can act on telemetry |
| CS | Consequence Severity | Represents consequence severity across governed domains |
| TE | Threat Exposure | Represents adversary pressure and exposure conditions |
| USOM | Unified Security Operations Metric | Represents operational execution and mitigation capability |
| RRAS | Resilience and Risk Assurance Score | Scalar structural-resilience summary |

The governing path is:

```text
TE + CS + R_j -> D_eff -> H -> R_inst
CM + USOM     -> M -------------^
R_inst + M    -> persistent stock S -> CRPI = max(R_inst, S)
```

The implementation mirrors the paper’s equations:

- resilience-adjusted consequence: `D_eff = sum(v_j D_j [1 - rho_j R_j])`, where each
  `R_j` is a domain-applicable resilience projection and scalar `RRAS` remains a
  reporting aggregate
- hazard pressure: `H = TE * D_eff`
- observability-modulated mitigation: `M = USOM * [m0 + (1 - m0) CM]`
- instantaneous residual posture: `R_inst = H * (1 - M)`
- persistent exposure: bounded exact stock-flow update with `beta`, `kappa`, and `dt`
- posture envelope: `CRPI = max(R_inst, S)`

Coverage is reported separately from posture. In addition to the Tier-2 aggregate and
minimum coverage diagnostics, the governing-path gate is
`C_gov = min(C_TE, C_CM, min_j C_Dj, min_j C_Rj, C_USOM)`. It is an evidence-completeness
qualification, not statistical confidence, and it never scales CRPI.

CRPI is scope-aware rather than executive-only. The same equations can be evaluated for
a component, sub-system, system, network, organizational domain, or enterprise. Parent
scores should use parent-scope evidence where available; a child-score average is a
separate roll-up and should be labelled as such.

The regularized geometric operator is zero-safe: one weak component contributes a
multiplicative penalty proportional to its governed weight without turning a non-zero
construct into an accidental absorbing zero.

## Formal verification and numerical conformance — Phases A–D

The [CRPI Formal Verification Protocol](docs/FORMAL_VERIFICATION_PROTOCOL.md) governs the mathematical scope, trusted axioms, version pins, source-to-manuscript correspondence, and release criteria.

**Phase A — Verified:** 11 Lean 4.24.0 theorem statements for elementary score algebra, consequence/hazard/mitigation/residual boundedness and the conditional posture envelope. [Archived evidence](verification/evidence/b50dea4aaf40cad56c42cff436d450278459efbf/summary.json) · [Proof ledger](formal/lean/PROOF_STATUS.md).

**Phase B — Verified (2026-10-22):** 24 additional Lean 4.24.0 statements for regularized geometric aggregation, zero-weight handling, endpoints, nonabsorbing zeros, and directional properties of the **composed instantaneous residual**. [Archived exact-revision evidence](verification/evidence/e457153dc5ac5b48b432b3a6fec57d492432b1bb/phase-b-summary.json) · [Claim-level status](formal/lean/PHASE_B_STATUS.md) · [Statement review](formal/lean/PHASE_B_STATEMENT_REVIEW.md).

**Phase C — Verified (2026-10-22):** 21 additional Lean 4.24.0 statements for bounded stock transitions, zero-rate identity, equilibrium, convergence and exact fixed-input cadence consistency. [Archived evidence](verification/evidence/9dab18ba0e7045c28754746a0ba61a2cb1d2e592/phase-c-summary.json) · [Claim-level status](formal/lean/PHASE_C_STATUS.md) · [Statement review](formal/lean/PHASE_C_STATEMENT_REVIEW.md).

**Phase D — Numerical conformance accepted (2026-10-22):** [Exact-revision evidence](verification/evidence/509c5ae448cddbcd062ad8c984c713d73c07c345/phase-d-summary.json) records 19/19 Python tests, 44 high-precision Decimal oracle fields, five invariants, 25 scenario rows and 56/56 repeated theorem axiom audits under pinned Lean 4.24.0. The [conformance ledger](verification/PHASE_D_STATUS.md) and [P1–P6 proof-coverage matrix](verification/PROOF_COVERAGE_MATRIX.md) distinguish supported mathematical claims from the paper's unformalized optional P6 derivative statement and broader empirical questions.

**Release boundary:** The required mathematical subclaims of Propositions 1–6 are machine-checked under documented hypotheses, and the Python implementation passed independently sourced numerical vectors. This is **not** a claim of empirically calibrated risk, breach probability, financial-loss prediction or universal floating-point correctness. Phase D's evidence collector did **not** run its optional PDF check. A separate Tectonic 0.17.0 compilation has since succeeded with zero TeX overfull/undefined/missing-character diagnostics, and the compiled artifact is tracked in the publication PR. [Full-page visual publication QA](https://github.com/jmsbooth/cyber-risk-posture-model/issues/5) is still a separate release gate.

To reproduce the machine-checked mathematical proofs (with Lean 4.24.0 and pinned Mathlib):

```bash
cd formal/lean
lake build
lake env lean CRPI/Audit.lean
lake env lean CRPI/AuditB.lean
lake env lean CRPI/AuditC.lean
```

To rerun the complete numerical and Lean evidence capture locally, use `python scripts/capture_phase_d.py` from the repository root. The `--with-tex` option attempts a separate manuscript PDF build only when Tectonic is available.

The PowerShell collectors `scripts/capture_phase_a.ps1`, `scripts/capture_phase_b.ps1` and `scripts/capture_phase_c.ps1` retain separate Lean verification artifacts; the Python `scripts/capture_phase_d.py` collector independently checks the reference model and repeats all 56 theorem audits. All accepted source revisions and dependencies are archived. Empirical validity remains outside these tests.

## Reproduce the artifact

The reference implementation uses only the Python standard library. Python 3.10 or
newer is recommended.

```bash
# Mathematical/unit checks
python3 -m unittest discover -v

# Machine-readable invariant report
python3 scripts/validate_model.py

# Run all synthetic scenarios and write decomposed CSV/JSON outputs
python3 scripts/run_scenarios.py
```

To compile the manuscript with a local TeX runtime:

```bash
tectonic --outdir paper/build paper/CRM_revised.tex
```

The Codex LaTeX environment’s bundled Tectonic 0.17.0 runtime has been smoke-tested
against this source. The build may emit ordinary first-pass cross-reference warnings
while Tectonic resolves references; the final PDF is produced at
`paper/build/CRM_revised.pdf`. A full TeX Live installation is not required for this
source.

## Synthetic use cases

`data/examples/scenarios.csv` intentionally exercises different model behaviors:

- `baseline` — stable posture and coverage;
- `threat_surge` — increased external and internal threat exposure raises hazard;
- `operational_recovery` — CM and USOM improve, reducing current posture while the
  persistent stock dissipates more slowly;
- `resilience_gap` — weakened resilience increases consequence-sensitive residual
  posture; and
- `evidence_gap` — model values remain calculable, but low availability-domain
  consequence/resilience coverage makes the final qualification `restricted`.

The scenario runner writes `artifacts/example_results.csv` and
`artifacts/example_summary.json`. These outputs are intentionally ignored by Git so
that every run is regenerated from the tracked inputs and profile. Each row includes
the scalar RRAS report, domain-specific resilience projections, decomposed CRPI state,
and three coverage diagnostics: aggregate coverage, minimum Tier-2 coverage, and
governing-path coverage (`coverage_gov`).

With the tracked illustrative profile, a run produces the following headline values:

| Scenario | Initial CRPI | Peak CRPI | Final CRPI | Coverage qualification |
| --- | ---: | ---: | ---: | --- |
| baseline | 0.160 | 0.160 | 0.160 | qualified |
| threat_surge | 0.133 | 0.248 | 0.167 | qualified |
| operational_recovery | 0.287 | 0.287 | 0.096 | qualified |
| resilience_gap | 0.157 | 0.212 | 0.180 | qualified |
| evidence_gap | 0.167 | 0.170 | 0.170 | restricted |

These are synthetic behavior demonstrations under `illustrative-v0.1`; they are not
organizational measurements.

## Repository layout

```text
paper/                 Manuscript source and local PDF build directory
models/                Dependency-light CRPI equations and validation helpers
config/                Versioned illustrative calibration profile
data/examples/         Synthetic, non-sensitive scenario inputs
scripts/               Reproducibility entry points
tests/                 Mathematical and statistical behavior checks
artifacts/              Local generated outputs (ignored)
```

## Validation boundary

The included checks cover boundedness, directional behavior, zero-safe aggregation,
consequence-specific resilience, exact-update cadence consistency, and deterministic
bootstrap plumbing for synthetic scenario summaries. They do not establish that CRPI
predicts incidents, loss, or breach probability.

Empirical validation remains a separate research phase and should use governed
historical or prospective organizational data, comparison with simpler additive
baselines, uncertainty propagation, calibration stability checks, and explicit
outcome definitions. The governing-path coverage gate is a hard evidence-completeness
diagnostic: it prevents scalar RRAS or CS coverage from hiding an unobserved consequence
or resilience domain. Coverage qualifies a result; it does not multiply or otherwise
change CRPI. Coverage is not a statistical confidence interval.

## Calibration and security posture

All parameters that can change interpretation are explicit and versioned in the
calibration profile: model/version identity, time unit, governed domain set, domain
weights, resilience primitive definitions, domain-projection weights `a_j`, mitigability
factors `rho_j`, normalization bounds, smoothing and regularization parameters,
missing-data and temporal-initialization policies, and evidence gates. Historical
outputs should remain associated with the profile that produced them; longitudinal or
cross-organizational comparisons require the same profile or an explicitly documented
recalculation. Do not place credentials, tokens, raw sensitive telemetry, or production
data in this repository.

## Citation

If you use the manuscript or reference implementation, cite:

> Booth, James. *A Dynamic, Decomposable Operational Cyber Risk Posture Index*.
> Research manuscript and reproducible reference implementation, 2026.

Before submission, adapt `paper/CRM_revised.tex` to the target venue’s template,
bibliography requirements, page limits, and artifact-availability policy.
