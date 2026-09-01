import json
import unittest
from pathlib import Path

from models.validation import bootstrap_mean_ci, run_invariant_checks


class ValidationTests(unittest.TestCase):
    def test_invariant_suite_passes(self):
        checks = run_invariant_checks()
        self.assertEqual(len(checks), 5)
        self.assertTrue(all(check["status"] == "pass" for check in checks))

    def test_bootstrap_is_reproducible(self):
        first = bootstrap_mean_ci([0.1, 0.2, 0.4, 0.5], iterations=200, seed=11)
        second = bootstrap_mean_ci([0.1, 0.2, 0.4, 0.5], iterations=200, seed=11)
        self.assertEqual(first, second)
        self.assertLessEqual(first[0], first[1])
        self.assertLessEqual(first[1], first[2])

    def test_calibration_profile_declares_model_governance(self):
        profile_path = Path(__file__).resolve().parents[1] / "config" / "calibration_baseline.json"
        profile = json.loads(profile_path.read_text(encoding="utf-8"))
        required = {
            "profile_id",
            "model_id",
            "model_version",
            "time_unit",
            "domain_set",
            "domain_definitions",
            "normalization",
            "smoothing",
            "resilience_primitive_definitions",
            "weights",
            "resilience_applicability",
            "resilience_applicability_policy",
            "missing_data_policy",
            "temporal_initialization_policy",
            "evidence_thresholds",
            "coverage_gates",
        }
        self.assertTrue(required.issubset(profile))
        self.assertEqual(set(profile["domain_set"]), set(profile["weights"]["consequence"]))
