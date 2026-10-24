"""Guardrails for the CRPI prospective study metadata/preflight (no real data)."""
from __future__ import annotations
import copy
import json
import unittest
from pathlib import Path
from models.pilot_readiness import assess_registration

ROOT = Path(__file__).resolve().parents[1]


def template():
    return json.loads((ROOT / "config/prospective_pilot_registration.example.json").read_text(encoding="utf-8"))


def synthetic_complete():
    p = template()
    p["stage"] = "frozen"
    g = p["governance"]
    g.update(participant_consent_status="approved", consent_receipt_ref="PRIVATE-CONSENT-RECEIPT",
             organizational_data_use_status="approved", data_use_receipt_ref="PRIVATE-DUA-RECEIPT",
             ethics_status="not_required", ethics_receipt_ref="PRIVATE-ETHICS-RECEIPT",
             private_storage_attested=True, private_storage_policy_ref="PRIVATE-STORAGE-RECEIPT")
    p["population"].update(scope_freeze_status="frozen", inventory_boundary_ref="PRIVATE-INVENTORY",
                           sampling_plan_ref="PRIVATE-SAMPLE-PLAN", dependency_cluster_policy_ref="PRIVATE-CLUSTERS")
    p["measurement"].update(definitions_frozen=True, two_blinded_impact_reviewers=True,
                            independent_source_audit=True, freeze_receipt_ref="PRIVATE-PROFILE-FREEZE")
    p["outcome"].update(adjudicator_blinded_to_scores=True, independently_sourced=True,
                        definition_ref="PRIVATE-CASE-DEF", adjudication_ref="PRIVATE-ADJUDICATION")
    p["holdout"].update(fixed_before_outcome_review=True, split_protocol_ref="PRIVATE-SPLIT-PLAN")
    p["analysis"].update(sample_size_rationale_ref="PRIVATE-POWER", metric_selection_ref="PRIVATE-METHODS",
                          missingness_analysis_ref="PRIVATE-MISSINGNESS", multiple_testing_ref="PRIVATE-CORRECTION")
    p["preregistration"].update(status="locked", locked_at="2027-01-01T00:00:00Z",
                                registry_ref="PRIVATE-REGISTRY-RECEIPT", independent_signoff_ref="PRIVATE-REVIEWER-RECEIPT")
    return p


class PilotReadinessTests(unittest.TestCase):
    def test_public_example_is_valid_but_blocked(self):
        report = assess_registration(template())
        self.assertTrue(report["structurally_valid"])
        self.assertFalse(report["documentary_gates_complete"])
        self.assertGreater(len(report["outstanding_gates"]), 10)
        self.assertFalse(report["study_authorized_or_empirically_validated"])

    def test_synthetic_complete_does_not_claim_external_authorization(self):
        report = assess_registration(synthetic_complete())
        self.assertTrue(report["structurally_valid"])
        self.assertTrue(report["documentary_gates_complete"])
        self.assertFalse(report["study_authorized_or_empirically_validated"])

    def test_reject_public_data_flag_and_row_injection(self):
        p = template(); p["governance"]["public_repository_contains_raw_data"] = True
        self.assertFalse(assess_registration(p)["structurally_valid"])
        p = template(); p["observations"] = [{"scope_id": "real"}]
        self.assertFalse(assess_registration(p)["structurally_valid"])

    def test_unknown_key_and_private_contacts_are_rejected(self):
        p = template(); p["governance"]["contacts"] = ["person@example.test"]
        self.assertFalse(assess_registration(p)["structurally_valid"])
        self.assertTrue(any("unexpected fields" in x for x in assess_registration(p)["structural_errors"]))
        p = template(); p["participant_name"] = "Do-not-include"
        self.assertFalse(assess_registration(p)["structurally_valid"])

    def test_prevent_frozen_lie(self):
        p = template(); p["stage"] = "frozen"
        r = assess_registration(p)
        self.assertFalse(r["structurally_valid"])

    def test_detect_outcome_temporal_leakage(self):
        p = synthetic_complete(); p["holdout"]["embargo_days"] = 2
        r = assess_registration(p)
        self.assertFalse(r["documentary_gates_complete"])
        self.assertTrue(any("embargo" in s for s in r["outstanding_gates"]))

    def test_reject_invalid_outcome_and_bad_days(self):
        p = template(); p["outcome"].update(primary_outcome="breach_probability", forward_horizon_days=0)
        self.assertFalse(assess_registration(p)["structurally_valid"])

    def test_missing_reference_blocks_complete(self):
        p = synthetic_complete(); p["analysis"]["sample_size_rationale_ref"] = None
        r = assess_registration(p)
        self.assertFalse(r["documentary_gates_complete"])
        self.assertFalse(r["structurally_valid"])  # frozen status inconsistent

    def test_digest_stable_independent_of_input_key_order(self):
        a = template(); b = json.loads(json.dumps(a, sort_keys=True))
        self.assertEqual(assess_registration(a)["manifest_sha256"],
                         assess_registration(b)["manifest_sha256"])

    def test_allows_opaque_private_approval_refs(self):
        p = synthetic_complete()
        for key, value in p["governance"].items():
            if key.endswith("_ref"):
                self.assertFalse(value.startswith("https://"))
        self.assertTrue(assess_registration(p)["documentary_gates_complete"])


if __name__ == "__main__":
    unittest.main()