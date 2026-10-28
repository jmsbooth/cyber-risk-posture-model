"""Phase D Python conformance against manuscript-derived independent Decimal vectors.

The high-precision oracle is independent of models.crm_reference, and declared
numeric tolerances are not Lean axioms or proofs over floating-point inputs.
"""
from __future__ import annotations

import json
import math
import random
import tempfile
import unittest
from decimal import Decimal, localcontext
from pathlib import Path

from models.crm_reference import (
    effective_consequence, evaluate_step, hazard_pressure, instantaneous_residual,
    mitigation, regularized_geometric, resilience_projection, simulate,
    update_persistent_stock, weighted_sum,
)
from scripts.regenerate_phase_d import regularized as decimal_geometric
from scripts.regenerate_phase_d import run as check_decimal_vectors
from scripts.run_scenarios import run as run_scenarios

ROOT = Path(__file__).resolve().parents[1]
VECTORS = json.loads((ROOT / "verification/reference_vectors.json").read_text(encoding="utf-8"))
ABS = float(VECTORS["absolute_tolerance"])
REL = float(VECTORS["relative_tolerance"])
DISPLAY = float(VECTORS["manuscript_rounded_tolerance"])


def floats(inputs: dict[str, str]) -> dict[str, float]:
    return {key: float(value) for key, value in inputs.items()}


class PhaseDConformanceTests(unittest.TestCase):
    def check_number(self, got: float, expected: str | float, name: str = "") -> None:
        self.assertTrue(math.isfinite(got), f"{name}: nonfinite {got}")
        self.assertTrue(math.isclose(got, float(expected), rel_tol=REL, abs_tol=ABS),
                        f"{name}: observed {got:.17g}, expected {expected}, tolerance {ABS}")

    def test_fixture_metadata_and_independent_decimal_oracle(self) -> None:
        self.assertEqual(VECTORS["schema_version"], "crpi-phase-d-v1")
        self.assertEqual(VECTORS["reference_profile"], "illustrative-v0.1")
        self.assertEqual(VECTORS["authority"], "paper/CRM_revised.tex")
        self.assertEqual(len(VECTORS["aggregation"]), 10)
        self.assertEqual(len(VECTORS["persistence"]), 8)
        for group in ("aggregation", "persistence"):
            names = [item["id"] for item in VECTORS[group]]
            self.assertEqual(len(names), len(set(names)))
        check_decimal_vectors(write=False)

    def test_regularized_aggregation_against_decimal_goldens(self) -> None:
        for item in VECTORS["aggregation"]:
            with self.subTest(vector=item["id"]):
                x = list(map(float, item["values"]))
                w = list(map(float, item["weights"]))
                eps = float(item["epsilon"])
                self.check_number(regularized_geometric(x, w, eps), item["expected"], item["id"])
                self.check_number(resilience_projection(x, w, eps), item["expected"],
                                  item["id"] + " domain")

    def test_manuscript_full_governing_path(self) -> None:
        data = VECTORS["worked_example"]
        x, e = data["inputs"], data["expected"]
        domains = floats(x["consequence_domains"])
        weights = floats(x["consequence_weights"])
        rho = floats(x["resilience_applicability"])
        r = floats(x["domain_resilience"])
        te = regularized_geometric(list(map(float, x["te_values"])),
                                   list(map(float, x["te_weights"])), float(x["epsilon_te"]))
        cs = weighted_sum([domains[k] for k in weights], [weights[k] for k in weights])
        d_eff = effective_consequence(domains, weights, rho, r)
        hazard = hazard_pressure(te, d_eff)
        m = mitigation(float((x["soe"] if "soe" in x else x["usom"])), float(x["cm"]), float(x["m0"]))
        residual = instantaneous_residual(hazard, m)
        stock = update_persistent_stock(float(x["stock_prev"]), residual, m,
                                        float(x["beta"]), float(x["kappa"]), float(x["dt"]))
        actual = dict(te=te, cs=cs, d_eff=d_eff, hazard=hazard, mitigation=m,
                      residual=residual, stock=stock, crpi=max(residual, stock),
                      q=float(x["beta"]) * residual + float(x["kappa"]) * m)
        actual["stock_equilibrium"] = float(x["beta"]) * residual / actual["q"]
        for name, expected in e.items():
            with self.subTest(intermediate=name):
                self.check_number(actual[name], expected, name)
        for name, rounded in data["manuscript_rounded"].items():
            with self.subTest(manuscript_label=name):
                self.assertLessEqual(abs(actual[name] - float(rounded)), DISPLAY)
        evaluated = evaluate_step(t=1.0, te=te, consequence_domains=domains,
                                  consequence_weights=weights, resilience_applicability=rho,
                                  domain_resilience=r, rras=float(x["rras_report_only"]),
                                  cm=float(x["cm"]), soe=float((x["soe"] if "soe" in x else x["usom"])), m0=float(x["m0"]),
                                  stock=float(x["stock_prev"]), beta=float(x["beta"]),
                                  kappa=float(x["kappa"]), dt=float(x["dt"]))
        for key in ("te", "cs", "d_eff", "hazard", "mitigation", "residual", "stock", "crpi"):
            self.check_number(getattr(evaluated, key), e[key], "evaluate_step." + key)
        self.assertEqual(evaluated.resilience_by_domain, r)
        self.assertEqual(evaluated.rras, float(x["rras_report_only"]))

    def test_scalar_rras_is_report_only(self) -> None:
        x = VECTORS["worked_example"]["inputs"]
        kw = dict(t=0.0, te=.598, consequence_domains=floats(x["consequence_domains"]),
                  consequence_weights=floats(x["consequence_weights"]),
                  resilience_applicability=floats(x["resilience_applicability"]),
                  domain_resilience=floats(x["domain_resilience"]),
                  cm=.725, soe=.6, m0=.25, stock=.2, beta=.3, kappa=.8, dt=1.0)
        low = evaluate_step(rras=0.0, **kw)
        high = evaluate_step(rras=1.0, **kw)
        for name in ("cs", "d_eff", "hazard", "mitigation", "residual", "stock", "crpi"):
            self.assertEqual(getattr(low, name), getattr(high, name), name)

    def test_persistent_stock_against_decimal_goldens(self) -> None:
        for v in VECTORS["persistence"]:
            with self.subTest(vector=v["id"]):
                actual = update_persistent_stock(float(v["stock"]), float(v["residual"]),
                                                 float(v["mitigation"]), float(v["beta"]),
                                                 float(v["kappa"]), float(v["dt"]))
                self.check_number(actual, v["expected_stock"], v["id"])
                self.assertGreaterEqual(actual, 0.0)
                self.assertLessEqual(actual, 1.0)

    def test_cadence_semigroup_at_valid_rates(self) -> None:
        cases = ((.2, .35, .4, .3, .8, .5, 1.5),
                 (0.0, 1.0, 0.0, .3, .8, 3.0, 2.0),
                 (1.0, 0.0, 1.0, .3, .8, .2, 7.0),
                 (.5, 0.0, 0.0, .3, .8, .5, 2.0),
                 (.5, .4, .6, 0.0, 0.0, 1.0, 2.0))
        for stock, residual, m, beta, kappa, t1, t2 in cases:
            with self.subTest(case=(stock, residual, m, beta, kappa)):
                direct = update_persistent_stock(stock, residual, m, beta, kappa, t1 + t2)
                split = update_persistent_stock(
                    update_persistent_stock(stock, residual, m, beta, kappa, t1),
                    residual, m, beta, kappa, t2)
                self.check_number(split, direct, "semigroup")

    def test_default_history_initialization_and_state_carry(self) -> None:
        x = VECTORS["worked_example"]["inputs"]
        row = {"t": 0.0, "te": .598, "consequence_domains": floats(x["consequence_domains"]),
               "rras": .65, "domain_resilience": floats(x["domain_resilience"]),
               "cm": .725, "soe": .6}
        rows = [row, {**row, "t": 1.0, "te": .4}]
        params = dict(consequence_weights=floats(x["consequence_weights"]),
                      resilience_applicability=floats(x["resilience_applicability"]),
                      m0=.25, beta=.3, kappa=.8, dt=1.0)
        series = simulate(rows, **params)
        self.assertEqual(len(series), 2)
        self.check_number(series[0].stock, series[0].residual, "state-neutral S(t0)")
        expected_next = update_persistent_stock(series[0].stock, series[1].residual,
                                                series[1].mitigation, .3, .8, 1.0)
        self.check_number(series[1].stock, expected_next, "carried state")
        explicit = simulate(rows[:1], initial_stock=.2, **params)
        self.check_number(explicit[0].stock, update_persistent_stock(
            .2, explicit[0].residual, explicit[0].mitigation, .3, .8, 1.0))

    def test_seeded_float_vs_independent_decimal_samples(self) -> None:
        rng = random.Random(20261022)
        with localcontext() as ctx:
            ctx.prec = 70
            for i in range(120):
                x = [rng.randrange(0, 101) / 100 for _ in range(3)]
                n = [rng.randint(0, 10) for _ in range(3)]
                if sum(n) == 0:
                    n[0] = 1
                total = sum(n)
                weights = [num / total for num in n]
                eps = (.001, .05, .4, .9)[i % 4]
                num = [Decimal(a) / Decimal(total) for a in n]
                oracle = decimal_geometric([str(value) for value in x],
                                            [str(weight) for weight in num], str(eps))
                observed = regularized_geometric(x, weights, eps)
                self.check_number(observed, float(oracle), f"sample:{i}")

    def test_reject_invalid_boundaries(self) -> None:
        invalid_geom = [
            ([0.5], [1.0], 0.0), ([0.5], [1.0], 1.0),
            ([0.5], [-1.0], 0.05), ([0.5], [0.9], 0.05),
            ([0.5], [1.0], math.nan), ([0.5], [1.0], math.inf),
            ([-0.01], [1.0], 0.05), ([1.01], [1.0], 0.05),
            ([0.5, .6], [1.0], 0.05), ([], [], 0.05),
        ]
        for values, weights, eps in invalid_geom:
            with self.subTest(invalid_geometric=(values, weights, eps)):
                with self.assertRaises(ValueError):
                    regularized_geometric(values, weights, eps)
        # The Python contract must not accept normalizations that can push
        # a valid bounded aggregate beyond one by more than roundoff.
        with self.assertRaises(ValueError):
            weighted_sum([1.0], [1.0 + 5e-10])
        with self.assertRaises(ValueError):
            regularized_geometric([1.0], [1.0 + 5e-10], 0.05)
        # Individually finite rates can overflow when their contributions
        # are summed; rejecting them is safer than a false finite equilibrium.
        with self.assertRaises(ValueError):
            update_persistent_stock(.2, 1.0, 1.0, 1e308, 1e308, 1.0)
        for invalid in (-.001, 1.001, math.nan, math.inf):
            with self.assertRaises(ValueError):
                update_persistent_stock(invalid, .3, .4, .3, .8, 1.0)
        for invalid in (-.1, math.nan, math.inf):
            with self.assertRaises(ValueError):
                update_persistent_stock(.2, .3, .4, invalid, .8, 1.0)
            with self.assertRaises(ValueError):
                update_persistent_stock(.2, .3, .4, .3, .8, invalid)

    def test_published_synthetic_scenario_headlines(self) -> None:
        with tempfile.TemporaryDirectory(prefix="crpi-phase-d-") as tmp:
            report = run_scenarios(ROOT / "data/examples/scenarios.csv",
                                   ROOT / "config/calibration_baseline.json", Path(tmp))
        self.assertEqual(report["profile_id"], VECTORS["reference_profile"])
        expected = VECTORS["readme_scenarios_rounded"]
        self.assertEqual(set(report["scenarios"]), set(expected))
        for name, fields in expected.items():
            with self.subTest(scenario=name):
                observed = report["scenarios"][name]
                for left, right in (("initial_crpi", "initial"),
                                    ("max", "peak"), ("final_crpi", "final")):
                    self.assertLessEqual(abs(observed[left] - float(fields[right])), DISPLAY,
                                         f"{name}.{left}: {observed[left]} != {fields[right]}")
                self.assertEqual(observed["final_coverage_qualification"], fields["qualification"])


if __name__ == "__main__":
    unittest.main()
