import unittest
from math import isclose

from models.crm_reference import (
    effective_consequence,
    hazard_pressure,
    instantaneous_residual,
    mitigation,
    regularized_geometric,
    resilience_projection,
    update_persistent_stock,
)


class CRPIReferenceTests(unittest.TestCase):
    def test_regularized_geometric_is_zero_safe_and_bounded(self):
        self.assertGreater(regularized_geometric([0.0, 0.8], [0.5, 0.5], 0.05), 0.0)
        self.assertEqual(regularized_geometric([0.0, 0.0], [0.5, 0.5], 0.05), 0.0)
        self.assertEqual(regularized_geometric([1.0, 1.0], [0.5, 0.5], 0.05), 1.0)

    def test_zero_weight_components_are_accepted(self):
        result = regularized_geometric([0.4, 0.0], [1.0, 0.0], 0.05)
        self.assertTrue(isclose(result, 0.4, rel_tol=1e-12, abs_tol=1e-12))

    def test_effective_consequence_respects_domain_applicability(self):
        domains = {"irreversible": 0.8, "recoverable": 0.8}
        weights = {"irreversible": 0.5, "recoverable": 0.5}
        before = effective_consequence(
            domains,
            weights,
            {"irreversible": 0.0, "recoverable": 0.0},
            {"irreversible": 0.0, "recoverable": 0.0},
        )
        after = effective_consequence(
            domains,
            weights,
            {"irreversible": 0.0, "recoverable": 1.0},
            {"irreversible": 0.0, "recoverable": 1.0},
        )
        self.assertLess(after, before)
        self.assertTrue(
            isclose(
                effective_consequence(
                    domains,
                    weights,
                    {"irreversible": 0.0, "recoverable": 0.0},
                    {"irreversible": 0.0, "recoverable": 0.0},
                ),
                before,
            )
        )

    def test_domain_projection_can_weight_resilience_primitives_differently(self):
        primitives = [0.9, 0.1]
        availability = resilience_projection(primitives, [0.9, 0.1], 0.05)
        confidentiality = resilience_projection(primitives, [0.1, 0.9], 0.05)
        self.assertGreater(availability, confidentiality)

    def test_core_outputs_are_bounded(self):
        d_eff = effective_consequence(
            {"confidentiality": 0.8, "integrity": 0.7, "availability": 0.6},
            {"confidentiality": 1 / 3, "integrity": 1 / 3, "availability": 1 / 3},
            {"confidentiality": 0.0, "integrity": 0.4, "availability": 0.9},
            {"confidentiality": 0.40, "integrity": 0.55, "availability": 0.65},
        )
        h = hazard_pressure(0.8, d_eff)
        m = mitigation(0.7, 0.8, 0.25)
        residual = instantaneous_residual(h, m)
        stock = update_persistent_stock(0.2, residual, m, 0.3, 0.8, 1.0)
        self.assertTrue(all(0.0 <= value <= 1.0 for value in (d_eff, h, m, residual, stock)))

    def test_exact_stock_update_is_cadence_consistent(self):
        full = update_persistent_stock(0.2, 0.35, 0.4, 0.3, 0.8, 2.0)
        half = update_persistent_stock(
            update_persistent_stock(0.2, 0.35, 0.4, 0.3, 0.8, 1.0),
            0.35,
            0.4,
            0.3,
            0.8,
            1.0,
        )
        self.assertTrue(isclose(full, half, rel_tol=1e-12, abs_tol=1e-12))
