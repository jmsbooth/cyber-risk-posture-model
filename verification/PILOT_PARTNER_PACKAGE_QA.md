# CRPI partner-qualification research packet — source and scope QA

**Date:** 2026-10-25  
**Issue:** [#9 — Prospective organizational measurement validity pilot](https://github.com/jmsbooth/cyber-risk-posture-model/issues/9)  
**Status:** **PASS** for a shareable, **nonbinding pre-data collection** research discussion packet. **NOT** empirical validation, participant qualification, IRB/ethics determination, authorization to collect data, or approval of any specific outcome/normalizer.

## Delivered artifacts

- [Discussion-stage participation brief](../docs/PILOT_PARTICIPATION_BRIEF.md): scope, privacy, possible partner roles and unsent sample first contact.
- [Non-sensitive 12-question feasibility screen](../docs/PILOT_PARTNER_FEASIBILITY_SCREENING.md): no request for actual inventory, incidents, people/asset identifiers or private data.
- [15-input field review charter](../docs/PILOT_15_INPUT_FIELD_AUDIT.md): source class, transform, 15-specific semantic threats, numerator/denominator, freshness, sample/time-cap and reviewer requirements.
- [Prospective outcome decision record](../docs/PILOT_OUTCOME_FEASIBILITY_DECISION.md): conditional selection criteria, circularity exclusions, delayed outcome windows, grouped forward holdout, missingness and analysis requirements; **primary outcome and horizon remain open**.
- [Private workspace and governance runbook](../docs/PILOT_PRIVATE_WORKSPACE_AND_AUTHORIZATION.md): authorization roles, access separation, sample agreement schedule, privacy/ethics determination and private/public artifact boundaries.
- Root README indexes all five documents without changing the existing public prereregistration template or model.

## Static acceptance checks and evidence

1. Fetched the canonical existing `config/measurement_pilot_v0.1.json` from `main`. Its **15** primitive identifiers correspond **exactly** to the 15 row identifiers in the audit charter (no omissions, substitutions or duplications). Its uncalibrated time-cap, min-sample and freshness parameters are described without being promoted to validated thresholds.
2. Fetched a recursive Git tree for the research branch (**122** files/directories, `truncated=false`). Checked the relative Markdown link targets in the README and all five new documents; **zero missing relative file targets**. External NIST/OHRP/OSF pointers were reviewed against their official documentation, not used to assert CRPI validity or automatic IRB applicability.
3. Checked the five new documents distinguish **candidate** future endpoints from preregistered or validated outcomes, avoid naming an actual participant or source record, and explicitly prohibit public raw organizational evidence. The participation outreach paragraph is **unsent**. No particular organization, contact, sponsor, data-use or ethics authority is claimed.
4. The current public `config/prospective_pilot_registration.example.json` remains an **unapproved draft**. Its previous exact-checkout preflight outcome was **26** outstanding gates and protective `--require-ready` exit **2**. **No rerun** of that command or the 48-test Python suite is claimed for this documentation-only increment.
5. GitHub diff scope must remain **README and `docs/` plus this verification record only**; no `paper/`, `models/`, `scripts/`, `tests/`, `config/`, `formal/lean/` or source data may be changed in this increment.

## Claim and decision boundary

**Ready:** organization-neutral initial feasibility conversation and human reviewer selection process.  
**Not ready:** recruitment/enrollment, actual evidence ingestion, consent/data-use/ethics approval, calibration or validated outcome association.

The next actionable blocker requires an actual willing organization with accountable sponsor and appropriate authority. Once found, its legal/data custodian must approve an organization-specific private workspace and data-use/ethics scope. Separately, field experts/statistician must review the 15 measures and freeze an outcome, measurement/profile policy, holdout and independent audit protocol before prospective outcome data are examined. The existing [prospective protocol](../docs/EMPIRICAL_VALIDATION_STUDY_PROTOCOL.md) and [metadata preflight](../docs/PROSPECTIVE_PILOT_STARTER_PACK.md) remain controlling.

**Scope-limited acceptance:** This QA establishes that the **research preparation packet** is internally linked and semantically bounded. It is **not** independent scientific peer review, external ethics approval, actual consent, data security attestation or validation of CRPI as an instrument.
