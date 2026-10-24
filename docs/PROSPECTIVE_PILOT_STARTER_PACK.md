# CRPI prospective organizational pilot — readiness pack v0.1

**Research stage: protocol/preparation only. No participants enrolled. No real organizational evidence or outcomes received. No external authorization is implied.** This work implements the pre-intake portion of [Issue #9](https://github.com/jmsbooth/cyber-risk-posture-model/issues/9). The governing CRPI equations, 15-field illustrative normalizer, Lean theorems, synthetic baselines and accepted 41-page manuscript are unchanged.

## What is ready now

1. A strictly metadata-only preregistration manifest template, `config/prospective_pilot_registration.example.json`. The example intentionally has **pending** consent, data-use, ethics, population, calibration, outcome and registration gates; it is **not** a registered study.
2. A reproducible preflight, `scripts/check_pilot_readiness.py`, which checks evidence of a prospective design and returns `structurally_valid`, `documentary_gates_complete`, explicit unmet requirements and a canonical SHA-256 over the manifest's JSON content. The latter is a reproducible fingerprint, **not an approved signature, timestamp or registry record**.
3. A conservative policy: synthetic and public documentation only in this repository; data-use agreements, real measurement records, inventories, security tickets, identifiers and outcome labels must remain in a **separate approved private environment**. A `.gitignore` rule is a safeguard against accidental commits, not an access-control boundary.
4. Ten standard-library regression tests for manifest structure, synthetic readiness, no public raw data, strict fields, blinded adjudication and temporal leakage checks.

## Execute the research preflight

From the repository root:

```bash
python scripts/check_pilot_readiness.py config/prospective_pilot_registration.example.json
python scripts/check_pilot_readiness.py config/prospective_pilot_registration.example.json --require-ready
python -m unittest discover -v
```

The first command should exit `0`, with `structurally_valid: true` and `documentary_gates_complete: false`. The second must exit **2** because the synthetic template has no participant approvals or registered design; that is the **expected safe failure**. Exit `1` indicates malformed or incompatible registration metadata. Even a `documentary_gates_complete: true` result verifies *only self-declared references and fields*, never legal authority, source credibility or scientific validity. Human approval and private-system verification must be performed separately.

Do **not** replace synthetic receipt IDs with real participant names, email addresses or public hyperlinks containing confidential details. Store only opaque references to private approvals. An external study registry and immutable governance record must retain the independently signed plan, its freeze time and actual authorized participants.

## Dependency map before first real observation

| Workstream | Scope and output | Release gate |
| --- | --- | --- |
| Pilot population | Consenting service owners, eligible assets, in-scope dependency clusters, exact inventory snapshots and stable denominators | Scope and selection-bias audit frozen |
| Data governance | Signed participant permission, organizational data-use authorization, ethics/IRB determination, approved workspace, retention/withdrawal policy | Human approval with private evidence receipts |
| 15 operational primitives | [Provisional normalizer profile](../config/measurement_pilot_v0.1.json), reviewed raw numerator/denominator definitions, anchored business-impact rubrics, event clocks, sample eligibility, owners and measurement profiles | Independent measurement and data-quality reviewer signoff |
| Outcome case definition | One preregistered primary future outcome independently observed, using a protocol-defined horizon; no outcome is directly derived from CRPI inputs | Blinded adjudicator, explicit source, severity/censoring criteria, and leakage audit |
| Split and analysis | Service/dependency-grouped **forward-time holdout** with embargo (at least the planned outcome horizon unless an independently justified non-overlap proof exists); predeclared simple baselines and uncertainty strategy | Locked split, power/precision rationale and analysis script outline before examining holdout labels |
| Preregistration | Canonical manifest digest, immutable registry entry, timestamps, independent approval receipts | Frozen before outcome inspection; subsequent changes must be versioned and marked exploratory |

### Private analysis data contract (illustrative design; do not commit real rows)

**Grain:** one pseudonymous `scope_token × measurement_window_end` measurement, joined only within the private approved workspace to a *later*, independently adjudicated outcome window. Use a separate table for source-evidence and denominator lineage and a separate table for outcome adjudication. At minimum the private schema should preserve these fields:

- **Study / scope identity:** `study_id`, `scope_token`, `dependency_cluster_token`, `measurement_window_start`, `measurement_window_end`, `measurement_profile_id`, `model_profile_id`, `inventory_snapshot_ref`.
- **Measured CRPI inputs:** 15 primitive name/value pairs, raw numerator/denominator/ordinal/time-quantile fields where applicable, units, original source reference, immutable source digest, observation and review timestamps, reviewer aliases, duplication/missingness reason, sample size, declared missing vs observed zero.
- **Stock and score lineage:** `R_inst`, `S_previous`, `dt_days`, `S_next`, `CRPI`, dominant envelope branch, history initialization mode, complete component decomposition, eligible-coverage fractions and source/profile hashes.
- **Independent future outcome:** `outcome_window_start`, `outcome_window_end`, `case_definition_version`, `outcome_status`, `adjudication_timestamp`, `adjudication_evidence_ref`, `reviewer_alias`, `censored_or_unknown`, `outcome_severity` where applicable. Do not include future outcome information in score generation or normalizer fitting for that measurement window.
- **Split designation:** a frozen `train/calibration/holdout` role, group key, timestamp and embargo logic that accounts for dependency overlap. Never let the same correlated service/dependency or overlapping future outcome appear across an improperly separated training and holdout set.

The above is a **design dictionary**, not a claim that actual private rows, schemas, connectors or participant records exist. Existing `models/operational_pilot.py` can evaluate individually governed observations, but it does **not** by itself authenticate source evidence, adjudicate outcomes, estimate uncertainty, fit calibrations or implement the prospective holdout analysis.

### Outcome candidate selection

The registration template proposes `independently_adjudicated_control_failure` within a **hypothetical** 28-day horizon. This is not a final outcome choice or a validated horizon. Alternatives include adjudicated security incidents, independently verified recovery-exercise outcomes and service interruptions. Before recruitment, an independent reviewer must assess how each can be recorded at feasible prevalence and **without circularly redefining the outcome from CRPI inputs**. Freeze one primary outcome. Do not silently combine unlike outcome types or treat scores as event probabilities.

### Measurement reliability and falsifiability

- Independently audit numerator **and** denominator inventories; capture selection and expansion biases. An asset count ratio may improve when previously unknown safe assets are discovered even if no control improves.
- Obtain two blinded ratings of each consequence domain and adjudicate differences; do not presume five ordinal levels have equal impact intervals.
- Record evidence IDs used in more than one construct. The pilot currently **reports duplicate IDs but does not reject them**; an independent reviewer must determine whether they inflate a single security effect.
- Time quantiles from ten cases are a *pilot gate*, not sufficient tail-estimation precision. Include non-detection, censored cases and event-time start/stop semantics in the prospective measurement plan.
- Separate missingness due to no observations, failing tools, out-of-scope controls and withheld evidence. Conditional feasible-value intervals are not confidence intervals or a full posterior model.
- Compare CRPI and preregistered baselines on the **same, appropriately eligible observations**, with service/time leakage controls. A higher CRPI correlation is not automatically a superior operational decision model; preserve null and negative findings.

## Next handoff — real-world approval needed

A participating organization or an explicitly authorized owner must choose the pilot system/service population and approve the use of evidence **in that organization's private workspace**. Then a domain security professional, business impact assessor, incident reviewer and statistician should freeze source mappings, outcomes and sampling protocol. Only after these controls are in place should actual observational data collection begin. The user's acceptance of this documentation or a local test run alone does not authorize that collection.

See [the prospective study protocol](EMPIRICAL_VALIDATION_STUDY_PROTOCOL.md) for the external-validity research design and [Issue #9](https://github.com/jmsbooth/cyber-risk-posture-model/issues/9) for the tracked gates. This package deliberately does **not** alter the accepted manuscript or claim new scientific results.