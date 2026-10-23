# CRPI operational input contract: minimum viable measurement and decomposition

**Status:** Proposed implementation specification for the existing CRPI v0.1 equations. The mathematical model, pinned illustrative profile, and reference Python are implemented. Raw-to-normalized measurement definitions and production calibration remain **unresolved**, so this contract does not certify organizational measurements.

## What the existing implementation actually accepts

The tracked `scripts/run_scenarios.py` takes **15 already normalized `[0,1]` values per interval**. It does **not** ingest raw vulnerability-management, identity, monitoring, incident, recovery or business-impact records. The `config/calibration_baseline.json` profile fixes weights, epsilon, resilience applicability, time units, temporal rates, and evidence thresholds, but its `normalization` object supplies **policies rather than raw `(L,U)` bounds for each actual measurement**. Appendix B of the manuscript describes supplementary metric tables as work that *should* be delivered; it is not a complete operational raw-input data dictionary. Real users currently must score many inputs through their own governed rubric.

The current scenario CSV also records **11 separately supplied evidence-coverage values**: `coverage_CM`, `coverage_CS`, `coverage_TE`, `coverage_USOM`, `coverage_RRAS`, three `coverage_D_<domain>` fields and three `coverage_R_<domain>` fields. The runner uses these only for coverage qualification, not to change CRPI. It does **not derive them automatically** from source inventories, evidence denominators, verification or freshness. Coverage must not be confused with statistical confidence.

### The explicit input hierarchy

```text
Source records (observed facts, timestamp, system/asset scope, provenance)
  -> Raw measurement (unit, declared L/U, higher-/lower-is-better, recency)
  -> Normalized primitive x in [0,1] (15 starter values)
       TE_external, TE_internal ----> G_epsilon,w ----> TE
       CS_conf, CS_integrity, CS_availability ---> D_j and reporting CS
       CM_coverage/freshness/integrity/verification --> mean --> CM
       USOM_detection/velocity/change_safety/learning --> mean --> USOM
       RRAS_internal/dependency --> G_epsilon,a_j --> R_C, R_I, R_A
                             \---> G_epsilon,reporting --> scalar RRAS (report only)
  -> D_eff = sum_j v_j D_j (1 - rho_j R_j)
  -> H = TE * D_eff; M = USOM * (m0 + (1 - m0) * CM)
  -> R_inst = H * (1 - M)
  -> S_next = exact stock transition(S_prior,R_inst,M,beta,kappa,dt)
  -> CRPI = max(R_inst,S_next)

Parallel evidence stream -> per-family and per-domain coverage -> qualification
(not a factor multiplying any risk/posture equation)
```

The `CM_*` and `USOM_*` arithmetic means and the two TE/RRAS primitive choices are specific to the *illustrative runner*, not a universal assertion that those four submetrics always have equal importance. A different implementation needs an explicit, version-controlled measurement/aggregation mapping consistent with the governing equation semantics.

## Three different notions of "minimum input"

| Operational state | Minimal mathematical inputs | Legitimate output | Limitation |
| --- | --- | --- | --- |
| **Algebraic screening** | Governed values for `TE`, `D_eff`, and `M` | `R_inst = TE*D_eff*(1-M)` | Only three numbers, but insufficient traceability to domains, resilience, monitoring or the contributing evidence; **not a complete organizational CRPI**. |
| **Decomposed instantaneous calculation** | `TE`, each `D_j`, each required `R_j`, `CM`, `USOM`; weights `v_j`, mitigability `rho_j`, baseline `m0` in a versioned profile | Decomposed `D_eff`, `H`, `M`, `R_inst`, and `CS` | In the three-domain illustrative profile, **eight** dynamic normalized values suffice because `rho_confidentiality=0`: 1 TE + 3 consequence + 2 effective resilience projections + CM + USOM. **Nine** are needed if all three `rho_j` are nonzero. Domain-specific measurement provenance remains mandatory. |
| **Starter evidence-level model** | All **15** currently declared normalized primitive values, the profile, and verifiable per-family/domain evidence coverage | Decomposed instant posture, reporting RRAS, and evidence qualification | Can produce an initial score from governed manual assessments only if those assessments have defensible definitions and normalization; the existing CSV is already scored synthetic input. |
| **Temporal CRPI** | Complete instant calculation plus **previous stock or an explicitly flagged cold start**, `beta`, `kappa`, `dt` in the same unit | `S_next`, `CRPI`, active envelope branch and temporal-history status | Setting `S(t0)=R_inst(t0)` is a neutral computational initialization, **not proof that no historical exposure exists**. A time series becomes increasingly informative as history accumulates. |
| **Missing required evidence** | Known normalized inputs, versioned admissible intervals for missing values, and provenance | Partial component scores, mathematical **possible-value interval** for `R_inst` where bounded endpoints can be computed, missing-input list and restricted qualification | Do not silently create a point-valued **fully qualified** CRPI by filling unknowns with 0, 0.5, or 1. If previous state is unknown, temporal CRPI cannot be identified from current measurements. An interval is not a confidence or probability interval. |

The 8-value minimum is profile-specific and refers to **already normalized/aggregated domain scores**, not eight raw telemetry counters. A resilience projection with `rho_j=0` is mathematically immaterial to `D_eff` but the current all-domain evidence gate still includes `C_Rj`. Treat this as a **coverage-governance design choice to review**, not a reason to silently remove domain evidence from operational reporting.

## Preliminary evidence-to-primitive examples, not calibration formulas

| Primitive group | Illustrative evidence an implementer could supply | Raw direction/normalization issue to govern |
| --- | --- | --- |
| `TE_external`, `TE_internal` | Confirmed exposed vulnerable services and attack surface; privileged access/exploitable identity and lateral-movement paths | More exploitable exposure means higher TE; define denominator, exploitability relevance, severity and exposure weighting. |
| `CS_confidentiality`, `CS_integrity`, `CS_availability` | Data classification/sensitivity inventory; transaction or mission integrity criticality; service dependency, RTO and continuity assessment | Higher business/mission consequence means larger `D_j`. Set stable impact classes with explicit interpretation, not CVSS copied directly into business consequence. |
| Four `CM_*` fields | Coverage of governed log/control sources; evidence freshness; tamper verification; evidence/control-state verification results | Higher verified observability/assurance is better. Declare expected sources, freshness windows, control universe and completeness denominators. |
| Four `USOM_*` fields | Detection and validation performance; measured response/remediation times; safe change implementation; demonstrated corrective-learning closure | Higher capability means better USOM. For raw MTTD, MTTR or failed-change counts, use appropriate lower-is-better normalization; do not confuse monitoring with execution. |
| `RRAS_internal`, `RRAS_dependency` | Recovery test evidence, redundancy and alternate path performance; supplier/third-party assurance, tested dependency recovery and change integrity | Higher demonstrated recoverability/assurance is better. Domain projection weights `a_j` and applicability `rho_j` are distinct governed parameters. |

The companion `config/operational_input_contract_v1.json` lists all 15 fields, proposed evidence classes, directional semantics and **explicitly missing raw normalization calibrations**. Empty or null raw bounds mean *unspecified*, not zero. A deployed organization needs a source owner and evidence mapping before claiming a calibrated measurement.

## Strict output contract

For each scoped entity and reporting interval, retain and expose:

1. `scope_id`, time interval and calibration `profile_id`/version; raw event source, origin and normalization policy for every primitive.
2. Validated primitive scores; `TE`, three `D_j`, each governing `R_j`, scalar `CS`, reporting-only `RRAS`, `CM`, `USOM`, `D_eff`, `H`, `M`, `R_inst`, `S_prior`, `S_next`, and `CRPI`; always show **which of `R_inst` or `S` controls the max envelope**.
3. Coverage by Tier 2 and consequence/resilience domain; aggregate, minimum and governing-path coverage; freshness/source-integrity qualification. Never multiply coverage into CRPI.
4. A list of unobserved, stale, manually assessed or imputed inputs, any numerical uncertainty bounds, and a clearly flagged cold-start history if used.
5. A full calculation lineage tying each output to measured evidence, weight/normalization version, and analytical scope. Cross-organization comparison requires compatible governed profiles, domain definitions and observation periods.

**Critical implementation distinction:** The current `config/calibration_baseline.json` uses `missing_data_policy = reject`; the manuscript permits optional governed LOCF, neutral and risk-averse imputation. These are **not the same policy**. The simulation below demonstrates why arbitrary neutral fill is not automatically safe. The production contract should default to reject/partial result with endpoint bounds, and permit an imputed point estimate only as a *clearly labeled secondary scenario* with a documented rule, not a measured CRPI.

## Before any real pilot

Define a metric dictionary with raw units, numerator, denominator, `(L,U)` boundaries, direction, source, owner, observation cadence, recency, evidence class, validation test, and no-data condition for every primitive. Validate each mapping with a human domain owner. Confirm business consequence and recovery meanings with mission/service owners. Establish the organizational unit of analysis, profile change-control and treatment of `rho_j = 0`. Test missingness and stale data with an independent reviewer. Then run in shadow mode before treating thresholds or trends as operational decisions.

**Research boundary:** This contract operationalizes the *existing* equation; it does not establish that its 15 example primitives, nominal parameter values or business consequence weights are calibrated or predictive for any actual organization.