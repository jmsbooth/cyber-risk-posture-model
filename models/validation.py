"""Mathematical and statistical validation helpers for the CRPI reference model."""

from __future__ import annotations

import random
from math import isclose
from statistics import mean
from typing import Callable, Iterable, Sequence

from .crm_reference import (
    effective_consequence,
    hazard_pressure,
    instantaneous_residual,
    mitigation,
    regularized_geometric,
    update_persistent_stock,
)


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def bootstrap_mean_ci(
    values: Sequence[float],
    *,
    iterations: int = 2000,
    confidence: float = 0.95,
    seed: int = 7,
) -> tuple[float, float, float]:
    """Return (lower, mean, upper) for a deterministic bootstrap mean interval.

    This helper is intended for synthetic scenario comparisons and uncertainty
    plumbing, not as a substitute for organizational outcome data.
    """

    if not values:
        raise ValueError("values must not be empty")
    if iterations < 1:
        raise ValueError("iterations must be positive")
    if not 0.0 < confidence < 1.0:
        raise ValueError("confidence must be in (0, 1)")
    rng = random.Random(seed)
    sample = tuple(float(value) for value in values)
    means = sorted(mean(rng.choice(sample) for _ in sample) for _ in range(iterations))
    alpha = (1.0 - confidence) / 2.0

    def percentile(q: float) -> float:
        position = q * (len(means) - 1)
        lower = int(position)
        upper = min(lower + 1, len(means) - 1)
        fraction = position - lower
        return means[lower] + fraction * (means[upper] - means[lower])

    return percentile(alpha), mean(sample), percentile(1.0 - alpha)


def finite_difference(
    function: Callable[[float], float], x: float, *, delta: float = 1e-5
) -> float:
    """Estimate a local derivative for a bounded sensitivity check."""

    if delta <= 0.0:
        raise ValueError("delta must be positive")
    return (function(x + delta) - function(x - delta)) / (2.0 * delta)


def run_invariant_checks() -> list[dict[str, object]]:
    """Run deterministic checks corresponding to the paper's validation objectives."""

    checks: list[tuple[str, Callable[[], None]]] = []

    def bounded_outputs() -> None:
        domains = {"confidentiality": 0.8, "integrity": 0.7, "availability": 0.6}
        weights = {key: 1.0 / 3.0 for key in domains}
        rho = {"confidentiality": 0.0, "integrity": 0.4, "availability": 0.9}
        d_eff = effective_consequence(
            domains,
            weights,
            rho,
            {"confidentiality": 0.40, "integrity": 0.55, "availability": 0.65},
        )
        h = hazard_pressure(0.8, d_eff)
        m = mitigation(0.7, 0.8, 0.25)
        residual = instantaneous_residual(h, m)
        stock = update_persistent_stock(0.2, residual, m, 0.3, 0.8, 1.0)
        _require(all(0.0 <= value <= 1.0 for value in (d_eff, h, m, residual, stock)), "CRPI state escaped [0, 1]")

    checks.append(("bounded outputs", bounded_outputs))

    def zero_safe_aggregation() -> None:
        _require(regularized_geometric([0.0, 0.8], [0.5, 0.5], 0.05) > 0.0, "single zero collapsed construct")
        _require(regularized_geometric([0.0, 0.0], [0.5, 0.5], 0.05) == 0.0, "all-zero input did not return zero")
        _require(regularized_geometric([1.0, 1.0], [0.5, 0.5], 0.05) == 1.0, "all-one input did not return one")

    checks.append(("zero-safe aggregation", zero_safe_aggregation))

    def directional_correctness() -> None:
        baseline = lambda te: instantaneous_residual(hazard_pressure(te, 0.6), 0.4)
        _require(finite_difference(baseline, 0.6) > 0.0, "TE should increase residual posture")
        mitigation_curve = lambda cm: instantaneous_residual(0.5, mitigation(0.7, cm, 0.25))
        _require(finite_difference(mitigation_curve, 0.5) < 0.0, "CM should reduce residual posture")

    checks.append(("directional correctness", directional_correctness))

    def consequence_specific_resilience() -> None:
        domains = {"irreversible": 0.8, "recoverable": 0.8}
        weights = {"irreversible": 0.5, "recoverable": 0.5}
        no_resilience_effect = {"irreversible": 0.0, "recoverable": 1.0}
        before = effective_consequence(
            domains,
            weights,
            no_resilience_effect,
            {"irreversible": 0.0, "recoverable": 0.0},
        )
        after = effective_consequence(
            domains,
            weights,
            no_resilience_effect,
            {"irreversible": 0.0, "recoverable": 1.0},
        )
        _require(after < before, "resilience should reduce applicable consequence")
        irreversible_only = {"irreversible": 0.0, "recoverable": 0.0}
        _require(
            isclose(
                effective_consequence(
                    domains,
                    weights,
                    irreversible_only,
                    {"irreversible": 0.0, "recoverable": 0.0},
                ),
                before,
            ),
            "non-applicable consequence changed",
        )

    checks.append(("consequence-specific resilience", consequence_specific_resilience))

    def cadence_consistency() -> None:
        full = update_persistent_stock(0.2, 0.35, 0.4, 0.3, 0.8, 2.0)
        half = update_persistent_stock(
            update_persistent_stock(0.2, 0.35, 0.4, 0.3, 0.8, 1.0),
            0.35,
            0.4,
            0.3,
            0.8,
            1.0,
        )
        _require(isclose(full, half, rel_tol=1e-12, abs_tol=1e-12), "cadence changed state trajectory")

    checks.append(("cadence consistency", cadence_consistency))

    results = []
    for name, check in checks:
        check()
        results.append({"name": name, "status": "pass"})
    return results


def summarize(values: Iterable[float]) -> dict[str, float]:
    """Provide stable descriptive statistics for a scenario output series."""

    materialized = tuple(float(value) for value in values)
    if not materialized:
        raise ValueError("values must not be empty")
    low, average, high = bootstrap_mean_ci(materialized)
    return {
        "min": min(materialized),
        "mean": average,
        "max": max(materialized),
        "bootstrap_mean_lower": low,
        "bootstrap_mean_upper": high,
    }
