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

## Proposed exact-source validation on the owner's Windows checkout

```powershell
git fetch origin
git switch --track origin/research/crpi-prospective-pilot-preflight
python scripts/check_pilot_readiness.py config/prospective_pilot_registration.example.json
python -m unittest discover -v
python scripts/check_pilot_readiness.py config/prospective_pilot_registration.example.json --require-ready
$LASTEXITCODE # expected 2 (a protective gate)
```

Do **not** mark the PR merged solely from the isolated Python tests. Perform exact-checkout regression, review metadata model semantics, preserve the no-real-data boundary and confirm correct README/Issue #9 links.

**Release boundary:** This PR prepares an eventual organizational validation study. The accepted 41-page CRPI manuscript, existing Lean theorems, canonical scoring functions and illustrative measurement calibration **must remain unchanged**. External pilot recruitment, permission, field measurements, blinded review and holdout analysis remain work for the consenting organization and [Issue #9](https://github.com/jmsbooth/cyber-risk-posture-model/issues/9).
