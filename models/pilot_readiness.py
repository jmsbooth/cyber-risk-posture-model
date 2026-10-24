"""Strict metadata-only preflight for prospective CRPI measurement studies.

This module does not ingest participant evidence or authorize collection.
A self-attested manifest can never substitute for consent, ethics or data-use approval.
"""
from __future__ import annotations

from datetime import datetime
from hashlib import sha256
from typing import Any, Mapping
import json

SCHEMA = "crpi-prospective-pilot-registration-v0.1"
FIELDS = {
    "root": {"schema", "study_id", "data_class", "stage", "unit_of_analysis", "governance", "population", "measurement", "outcome", "holdout", "analysis", "preregistration"},
    "governance": {"participant_consent_status", "consent_receipt_ref", "organizational_data_use_status", "data_use_receipt_ref", "ethics_status", "ethics_receipt_ref", "private_storage_attested", "private_storage_policy_ref", "public_repository_contains_raw_data"},
    "population": {"scope_freeze_status", "inventory_boundary_ref", "sampling_plan_ref", "dependency_cluster_policy_ref"},
    "measurement": {"measurement_profile_id", "model_profile_id", "definitions_frozen", "two_blinded_impact_reviewers", "independent_source_audit", "freeze_receipt_ref"},
    "outcome": {"primary_outcome", "forward_horizon_days", "adjudicator_blinded_to_scores", "independently_sourced", "definition_ref", "adjudication_ref"},
    "holdout": {"group_by_service_and_dependency", "forward_only", "embargo_days", "fixed_before_outcome_review", "split_protocol_ref"},
    "analysis": {"predeclared_comparators", "sample_size_rationale_ref", "metric_selection_ref", "missingness_analysis_ref", "multiple_testing_ref"},
    "preregistration": {"status", "locked_at", "registry_ref", "independent_signoff_ref"},
}

CANDIDATE_OUTCOMES = {
    "independently_adjudicated_control_failure",
    "prospective_service_interruption",
    "independently_adjudicated_security_incident",
    "verified_recovery_exercise_result",
}


def _nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _object(data: Mapping[str, Any], key: str, errors: list[str]) -> dict[str, Any]:
    item = data.get(key)
    if not isinstance(item, dict):
        errors.append(f"{key}: must be an object")
        return {}
    unexpected = set(item) - FIELDS[key]
    if unexpected:
        errors.append(f"{key}: unexpected fields: {', '.join(sorted(unexpected))}")
    return item


def _iso(text: Any) -> bool:
    if not _nonempty(text):
        return False
    try:
        timestamp = datetime.fromisoformat(text.replace("Z", "+00:00"))
        return timestamp.tzinfo is not None and timestamp.utcoffset() is not None
    except (ValueError, TypeError):
        return False


def _reference(value: Any) -> bool:
    # Reference is an opaque internal receipt ID; never require a public URL.
    return _nonempty(value) and len(value) <= 256


def _canonical_digest(value: Mapping[str, Any]) -> str:
    wire = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return sha256(wire.encode("utf-8")).hexdigest()


def assess_registration(plan: Mapping[str, Any]) -> dict[str, Any]:
    """Check structural validity and documentary gates without claiming external verification."""
    errors: list[str] = []
    pending: list[str] = []
    if not isinstance(plan, dict):
        raise ValueError("registration must be a JSON object")
    unexpected_root = set(plan) - FIELDS["root"]
    if unexpected_root:
        errors.append(f"root: unexpected fields: {', '.join(sorted(unexpected_root))}")
    if plan.get("schema") != SCHEMA:
        errors.append(f"schema: expected {SCHEMA}")
    if not _nonempty(plan.get("study_id")):
        errors.append("study_id: nonempty study identifier required")
    if plan.get("data_class") != "study_metadata_only":
        errors.append("data_class: only study_metadata_only permitted in public repo")
    if plan.get("stage") not in ("draft", "frozen"):
        errors.append("stage: must be draft or frozen")
    if plan.get("unit_of_analysis") != "service_window":
        errors.append("unit_of_analysis: expected service_window")
    # Public manifest must never embed individual service enrollment or outcome records.
    for forbidden in ("participants", "observations", "outcome_rows", "source_records", "contacts"):
        if forbidden in plan:
            errors.append(f"{forbidden}: prohibited in public preregistration metadata")

    governance = _object(plan, "governance", errors)
    if governance.get("public_repository_contains_raw_data") is not False:
        errors.append("governance.public_repository_contains_raw_data: must be false")
    if governance.get("participant_consent_status") != "approved":
        pending.append("participant consent and participation agreements must be approved")
    elif not _reference(governance.get("consent_receipt_ref")):
        pending.append("record an opaque consent approval reference in the approved private workspace")
    if governance.get("organizational_data_use_status") != "approved":
        pending.append("organizational data-use agreement must be approved")
    elif not _reference(governance.get("data_use_receipt_ref")):
        pending.append("record an opaque organizational data-use approval reference")
    if governance.get("ethics_status") not in ("approved", "not_required"):
        pending.append("ethics/IRB determination pending")
    elif not _reference(governance.get("ethics_receipt_ref")):
        pending.append("record ethics/IRB determination reference even if not required")
    if governance.get("private_storage_attested") is not True:
        pending.append("approved private storage and retention controls not attested")
    elif not _reference(governance.get("private_storage_policy_ref")):
        pending.append("private storage/retention policy reference missing")

    scope = _object(plan, "population", errors)
    if scope.get("scope_freeze_status") != "frozen":
        pending.append("scope population, eligible unit and denominator policy not frozen")
    if not _reference(scope.get("inventory_boundary_ref")):
        pending.append("inventory and service-boundary definition reference missing")
    if not _reference(scope.get("sampling_plan_ref")):
        pending.append("sampling and selection-bias protocol reference missing")
    if not _reference(scope.get("dependency_cluster_policy_ref")):
        pending.append("service/dependency cluster policy reference missing")

    measurement = _object(plan, "measurement", errors)
    if not _nonempty(measurement.get("measurement_profile_id")):
        errors.append("measurement.measurement_profile_id: required")
    if not _nonempty(measurement.get("model_profile_id")):
        errors.append("measurement.model_profile_id: required")
    if measurement.get("definitions_frozen") is not True:
        pending.append("15 raw measurement definitions, denominators and normalization anchors must be frozen")
    if measurement.get("two_blinded_impact_reviewers") is not True:
        pending.append("independent blinded consequence-rubric reviewers missing")
    if measurement.get("independent_source_audit") is not True:
        pending.append("source inventory and numerator/denominator audit procedure missing")
    if not _reference(measurement.get("freeze_receipt_ref")):
        pending.append("versioned measurement-definition/profile freeze receipt missing")

    outcome = _object(plan, "outcome", errors)
    if outcome.get("primary_outcome") not in CANDIDATE_OUTCOMES:
        errors.append("outcome.primary_outcome: unknown or undefined outcome family")
    horizon = outcome.get("forward_horizon_days")
    if isinstance(horizon, bool) or not isinstance(horizon, int) or horizon <= 0:
        errors.append("outcome.forward_horizon_days: positive integer required")
    if outcome.get("adjudicator_blinded_to_scores") is not True:
        pending.append("outcome adjudicator must be blinded to CRPI scores")
    if outcome.get("independently_sourced") is not True:
        pending.append("outcome must be independently sourced, not derived from CRPI inputs")
    if not _reference(outcome.get("definition_ref")):
        pending.append("prospectively fixed outcome case definition reference missing")
    if not _reference(outcome.get("adjudication_ref")):
        pending.append("outcome adjudication and censoring policy reference missing")

    split = _object(plan, "holdout", errors)
    if split.get("group_by_service_and_dependency") is not True:
        pending.append("service/dependency-aware holdout grouping not specified")
    if split.get("forward_only") is not True:
        pending.append("forward-in-time holdout split not specified")
    embargo = split.get("embargo_days")
    if isinstance(embargo, bool) or not isinstance(embargo, int) or embargo < 0:
        errors.append("holdout.embargo_days: nonnegative integer required")
    elif isinstance(horizon, int) and not isinstance(horizon, bool) and embargo < horizon:
        pending.append("holdout embargo shorter than outcome horizon; demonstrate no outcome overlap or increase embargo")
    if split.get("fixed_before_outcome_review") is not True:
        pending.append("training/holdout separation must be frozen before outcome review")
    if not _reference(split.get("split_protocol_ref")):
        pending.append("predeclared split and leakage-audit policy reference missing")

    analysis = _object(plan, "analysis", errors)
    expected = {"crpi", "instantaneous_residual", "simple_additive", "arithmetic_te_ablation", "evidence_only"}
    controls = analysis.get("predeclared_comparators")
    if not isinstance(controls, list) or any(not isinstance(x, str) for x in controls):
        errors.append("analysis.predeclared_comparators: array of comparator identifiers required")
    elif not expected.issubset(set(controls)):
        pending.append("predeclare CRPI, three structural comparisons and evidence-only baseline")
    for key, meaning in [
        ("sample_size_rationale_ref", "sample-size/power or precision rationale"),
        ("metric_selection_ref", "primary association and interval method"),
        ("missingness_analysis_ref", "missingness/censoring and complete-case policy"),
        ("multiple_testing_ref", "multiple-comparison policy and practical effect size")
    ]:
        if not _reference(analysis.get(key)):
            pending.append(f"predeclare {meaning} ({key})")

    prereg = _object(plan, "preregistration", errors)
    if prereg.get("status") != "locked":
        pending.append("study preregistration not locked before source/outcome inspection")
    if not _iso(prereg.get("locked_at")):
        pending.append("timezone-aware preregistration lock time missing")
    if not _reference(prereg.get("registry_ref")):
        pending.append("immutable preregistration registry/receipt reference missing")
    if not _reference(prereg.get("independent_signoff_ref")):
        pending.append("independent scientific/ethics governance signoff reference missing")

    # Frozen status without completed preflight is a material inconsistency.
    if plan.get("stage") == "frozen" and (errors or pending):
        errors.append("stage=frozen conflicts with incomplete readiness gates")
    return {
        "schema": "crpi-prospective-pilot-preflight-v0.1",
        "study_id": plan.get("study_id"),
        "manifest_sha256": _canonical_digest(plan),
        "structurally_valid": not errors,
        "documentary_gates_complete": not errors and not pending,
        "study_authorized_or_empirically_validated": False,
        "structural_errors": errors,
        "outstanding_gates": pending,
        "note": "Self-attested metadata is not proof of consent, source integrity or IRB approval; a separate authorized human review is required before collecting data.",
    }