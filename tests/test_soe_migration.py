"""Canonical SOE identity and historical USOM v0.1 reproducibility contract."""
import json
import tempfile
import unittest
from pathlib import Path

from models.crm_reference import evaluate_step, mitigation, simulate
from models.operational_pilot import evaluate
from scripts.run_scenarios import run

ROOT = Path(__file__).resolve().parents[1]


def load(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


class SOEMigrationTests(unittest.TestCase):
    def setUp(self):
        self.calibration = load("config/calibration_baseline.json")

    def test_equation_and_output_use_canonical_soe(self):
        self.assertAlmostEqual(mitigation(soe=0.6, cm=0.725, m0=0.25), 0.47625)
        vectors = load("verification/reference_vectors.json")["worked_example"]["inputs"]
        self.assertIn("usom", vectors, "historical fixture must remain unchanged")
        self.assertNotIn("soe", vectors)
        from scripts.regenerate_phase_d import compute_worked
        outputs = compute_worked(vectors)
        self.assertAlmostEqual(float(outputs["mitigation"]), mitigation(0.6, 0.725, 0.25))
        domain = {k:float(v) for k,v in vectors["consequence_domains"].items()}
        weights = {k:float(v) for k,v in vectors["consequence_weights"].items()}
        rho = {k:float(v) for k,v in vectors["resilience_applicability"].items()}
        projection = {k:float(v) for k,v in vectors["domain_resilience"].items()}
        result = evaluate_step(
            t=0, te=0.5980818586266033, consequence_domains=domain,
            consequence_weights=weights, resilience_applicability=rho,
            domain_resilience=projection, rras=0.65, cm=0.725, soe=0.6,
            m0=0.25, stock=0.2, beta=0.3, kappa=0.8, dt=1.0,
        )
        self.assertIn("soe", result.as_dict())
        self.assertNotIn("usom", result.as_dict())
        self.assertEqual(result.usom, result.soe)

    def test_pilot_legacy_and_canonical_evaluate_identically(self):
        legacy = evaluate(
            load("data/examples/operational_pilot_case.json"),
            load("config/measurement_pilot_v0.1.json"), self.calibration)
        current = evaluate(
            load("data/examples/operational_pilot_case_soe.json"),
            load("config/measurement_pilot_soe_v0.2.json"), self.calibration)
        self.assertEqual(legacy["point"], current["point"])
        self.assertEqual(legacy["normalized_inputs"], current["normalized_inputs"])
        self.assertEqual(legacy["coverage"], current["coverage"])
        self.assertNotIn("USOM", current["point"])
        self.assertIn("SOE", current["point"])

    def test_conflicting_aliases_fail_closed(self):
        doc = load("data/examples/operational_pilot_case_soe.json")
        doc["observations"]["USOM_detection"] = doc["observations"]["SOE_detection"]
        with self.assertRaisesRegex(ValueError, "conflicting legacy/canonical"):
            evaluate(doc, load("config/measurement_pilot_soe_v0.2.json"), self.calibration)
        row={"t":0, "te":0.2,"rras":0.3,"cm":0.5,
             "domain_resilience":{"confidentiality":0.4,"integrity":0.4,"availability":0.4},
             "consequence_domains":{"confidentiality":0.5,"integrity":0.5,"availability":0.5},
             "soe":0.6,"usom":0.2}
        with self.assertRaisesRegex(ValueError, "either soe or historical usom"):
            simulate([row], consequence_weights=self.calibration["weights"]["consequence"],
                     resilience_applicability=self.calibration["resilience_applicability"],
                     m0=self.calibration["m0"], beta=self.calibration["beta"],
                     kappa=self.calibration["kappa"], dt=1.0)

    def test_scenario_csv_numeric_parity(self):
        with tempfile.TemporaryDirectory() as d:
            archive = run(ROOT/"data/examples/scenarios.csv",
                          ROOT/"config/calibration_baseline.json", Path(d)/"old")
            current = run(ROOT/"data/examples/scenarios_soe.csv",
                          ROOT/"config/calibration_baseline.json", Path(d)/"new")
            self.assertEqual(archive["scenarios"], current["scenarios"])


if __name__ == "__main__":
    unittest.main()
