# CRPI prospective study readiness — pre-intake evidence

**Status:** DRAFT / PREPARATION ONLY. Issue [#9](https://github.com/jmsbooth/cyber-risk-posture-model/issues/9) remains open; **no consenting participant, independently audited organizational measurement, incident label, calibrated score, field dataset or external approval** is claimed.

**Date:** 2026-10-24  
**Scope:** Prospective preregistration and intake-readiness metadata, not CRPI mathematical research or outcome analysis.

## Implemented

- Strict study-registration metadata gate: `models/pilot_readiness.py`, `scripts/check_pilot_readiness.py`.
- Deliberately incomplete but structurally valid [registration example](../config/prospective_pilot_registration.example.json).
- Human operating and independent-data-trust requirements in [the field-readiness pack](../docs/PROSPECTIVE_PILOT_STARTER_PACK.md).
- .gitignore safeguards for common locally stored private study directories. These are **not** access control and do not authorize committing regulated data.
- Test coverage for public-record leakage prevention, structure, frozen-plan contradictions, blind outcome review, forward-time embargoes, metadata hashing, empty consent references, future lock timestamps and self-attestation limits.

## Actual execution evidence

In an **isolated local Python 3.13.5 source tree**, the new preregistration tests returned **11/11 PASS** under `python -m unittest discover -v -s tests -p test_pilot_readiness.py`. This is **not a GitHub CI result** and **does not attest exact-source execution against the owner's Windows checkout**. The current `main` repository has 37 previously accepted tests; an owner's full-suite rerun on the candidate branch should report **48 tests** if no other tests have been added.

The example manifest preflight produced:
- `structurally_valid: true`;
- `documentary_gates_complete: false`;
- `study_authorized_or_empirically_validated: false`;
- 26 explicit pending documentary/governance gates;
- mandatory `--require-ready` invocation exits **2** (expected block).

**Important:** Even a hypothetical metadata manifest with all approval-reference fields filled cannot externally verify the referenced permission. A successful document preflight is **not legal authority** to collect private records, nor proof of security source validity, empirical CRPI discrimination, or calibration.

## Owner-local exact-source Windows acceptance — PASSED (2026-10-24)

The repository owner fetched and switched to the published PR branch at source revision **`c7995e2cc69a91339a321c55a83b9fbf6a2c4215`**, then executed the full suite and both modes of the metadata validator directly from the Windows repository checkout. These are **user-supplied PowerShell console results**, not a CI run, attested test log, real-data audit or independent authorization decision.

| Command / gate | Verified output |
| --- | --- |
| `python scripts/check_pilot_readiness.py config/prospective_pilot_registration.example.json` | `structurally_valid: true`, `structural_errors: []`, `documentary_gates_complete: false`, `study_authorized_or_empirically_validated: false`, **26** outstanding gates |
| Manifest canonical digest | `c869b76339d3084802671d97e091b45bf78c16e0a844191f668f3cd18a41a992` |
| `python -m unittest discover -v` | **`Ran 48 tests in 5.526s\nOK`**; 11 new preflight tests and 37 previously accepted tests passed |
| Phase D independent numerical oracle within same suite | **44 expected Decimal fields verified**, as reported by the conformance test |
| `python scripts/check_pilot_readiness.py config/prospective_pilot_registration.example.json --require-ready` | Mandatory readiness enforcement **blocked**, PowerShell `$LASTEXITCODE=2`, as designed |
| Study governance and real-data collection | **Not authorized**; the expected refusal correctly remains active |

**Interpretation:** The validator distinguishes a structurally valid *draft* from documentary completeness, and always states that metadata cannot independently verify consent, an ethics determination, source integrity or empirical validity. A code-level green check, including 48/48 tests, does **not** satisfy any of the 26 substantive approval/study-design gates; the parent [Issue #9](https://github.com/jmsbooth/cyber-risk-posture-model/issues/9) remains open.

**Semantic code review:** `models/pilot_readiness.py` restricts root and nested manifest keys, requires `data_class: study_metadata_only`, rejects the `public_repository_contains_raw_data=true` declaration, validates time-aware pre-registration metadata and holdout restrictions, and permanently emits `study_authorized_or_empirically_validated=false`. It checks only *self-declared* approval receipt references, not source authenticity or human authorization. `scripts/check_pilot_readiness.py` exits 2 when documentary requirements are incomplete with `--require-ready`; its normal default mode permits reviewing a valid incomplete draft. `.gitignore` safeguards are partial accidental-commit protection, not enforceable private-data security. These limitations are deliberate and must remain explicit.

**Acceptance decision:** **PASS for research-preparation tooling and exact-source Windows testing**. Eligible for merge into `main` *without closing Issue #9 or marking a study authorized*. No changes to `paper/CRM_revised.tex`, its accepted PDF, core model equations, calibration, Lean theorem source, or prior synthetic result corpus.

## Executed Windows acceptance commands

```powershell
git fetch origin
git switch --track origin/research/crpi-prospective-pilot-preflight
python scripts/check_pilot_readiness.py config/prospective_pilot_registration.example.json
python -m unittest discover -v
python scripts/check_pilot_readiness.py config/prospective_pilot_registration.example.json --require-ready
$LASTEXITCODE # expected 2 (a protective gate)
```

The required full-suite checkout replay and bounded semantic review are now documented above. The remaining **actual human/organizational approval and field-validity gates** must be completed through Issue #9 before any data collection or empirical-CRPI claims.

**Release boundary:** This PR prepares an eventual organizational validation study. The accepted 41-page CRPI manuscript, existing Lean theorems, canonical scoring functions and illustrative measurement calibration **must remain unchanged**. External pilot recruitment, permission, field measurements, blinded review and holdout analysis remain work for the consenting organization and [Issue #9](https://github.com/jmsbooth/cyber-risk-posture-model/issues/9).
