# SOE canonical naming migration (research v0.2)

The five Tier 2 constructs are CM, CS, TE, **Security Operations Effectiveness (SOE)**, and RRAS. SOE replaces the former **Unified Security Operations Metric (USOM)** without changing its normalized meaning or the governing equations. The effective-mitigation equation is now `M = SOE * [m0 + (1-m0)*CM]`. All four primitive inputs use `SOE_detection`, `SOE_velocity`, `SOE_change_safety`, and `SOE_learning`.

## Canonical artifacts

- `paper/CRM_revised.tex` is the active revised manuscript with SOE in all equations, labels, graphs and definitions.
- `models/crm_reference.py` uses `soe` as its canonical Python function parameter and serialized result key; a read-only `CRPIResult.usom` alias is retained for historical in-memory users.
- `models/operational_pilot.py` returns `SOE` and canonical input/evidence/coverage keys. Historical v0.1 primitive keys are accepted **only at the data input boundary**, with explicit collision rejection; no mixed/ambiguous key silently wins.
- `config/calibration_soe_v0.2.json`, `config/measurement_pilot_soe_v0.2.json`, `config/operational_input_contract_soe_v0.2.json`, `data/examples/scenarios_soe.csv`, and `data/examples/operational_pilot_case_soe.json` are the canonical examples.
- `formal/lean/CRPI/Mitigation.lean` and `formal/lean/CRPI/Direction.lean` now use SOE parameter and theorem names; these exact renamed sources require a new machine-check receipt.

## Reproducibility and legacy boundary

The original 2026 v0.1 calibration, raw pilot and scenario files, reference vectors, synthetic stress-result JSON, archived audit logs, and published 41-page PDF remain in place. They are **historical evidence tied to earlier source revisions**, not mislabeled canonical v0.2 releases. The legacy field and weight identifiers inside those frozen files are intentional.

The current stress and pilot comparison scripts normalize only the historical identifier difference when checking numerical parity. A matching historical synthetic result proves **rename equivalence**, not a new measurement or a newly validated model. A model consumer relying on the old `evaluate_step(usom=...)` signature must migrate to `evaluate_step(soe=...)`; the old result attribute remains temporarily available for read-only compatibility.

SOE is the capability to execute security-relevant operations across detection, response, remediation, change safety and improvement. It is not limited to a traditional Security Operations Center.

Publication and implementation acceptance must rerun Python tests, independent Decimal conformance, Lean proofs/audits, LaTeX compilation and PDF visual QA on the **same revision**. No organizational data, empirical calibration, institution affiliation, or independent referee signoff is implied by this migration.
