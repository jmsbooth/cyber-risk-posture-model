"""Dependency-light reference equations for the Cyber Risk Posture Index (CRPI).

The functions in this module mirror the governing equations in
``paper/CRM_revised.tex``. They intentionally avoid a numerical stack so that the
mathematical behavior can be tested in a clean Python environment. Inputs are
validated at the boundary and outputs are clamped only for floating-point roundoff.

This is a reference model, not an empirical breach-probability or financial-loss
model. Calibration values belong in a versioned profile such as
``config/calibration_baseline.json``.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from math import exp, expm1, isfinite, log, log1p
from typing import Iterable, Mapping, Sequence


def _bounded(value: float, name: str) -> float:
    """Return a finite value in [0, 1], or raise a useful boundary error."""

    value = float(value)
    if not isfinite(value) or not 0.0 <= value <= 1.0:
        raise ValueError(f"{name} must be finite and in [0, 1]; got {value!r}")
    return value


def _nonnegative_rate(value: float, name: str) -> float:
    value = float(value)
    if not isfinite(value) or value < 0.0:
        raise ValueError(f"{name} must be a finite non-negative rate; got {value!r}")
    return value


def _validate_weights(weights: Sequence[float], expected_length: int) -> tuple[float, ...]:
    if len(weights) != expected_length or not weights:
        raise ValueError("weights must have the same non-zero length as values")
    normalized = tuple(float(weight) for weight in weights)
    if any(not isfinite(weight) or weight < 0.0 for weight in normalized):
        raise ValueError("weights must be finite and non-negative")
    # A looser tolerance can admit a sum above one by more than the
    # permitted output-roundoff guard, violating the bounded-score contract.
    if abs(sum(normalized) - 1.0) > 1e-12:
        raise ValueError(f"weights must sum to 1; got {sum(normalized)!r}")
    return normalized


def _clamp_roundoff(value: float) -> float:
    if abs(value) <= 1e-12:
        return 0.0
    if 1.0 <= value <= 1.0 + 1e-12:
        return 1.0
    return value


def weighted_sum(values: Sequence[float], weights: Sequence[float]) -> float:
    """Compute a bounded weighted sum for compensatory construct components."""

    checked_values = tuple(_bounded(value, "value") for value in values)
    checked_weights = _validate_weights(weights, len(checked_values))
    return _clamp_roundoff(sum(value * weight for value, weight in zip(checked_values, checked_weights)))


def regularized_geometric(
    values: Sequence[float], weights: Sequence[float], epsilon: float
) -> float:
    """Compute the zero-safe regularized weighted geometric operator.

    This is Equation (1) in the paper:

    ``(prod(epsilon + (1-epsilon) * x_i) ** w_i - epsilon) / (1-epsilon)``.
    """

    checked_values = tuple(_bounded(value, "value") for value in values)
    checked_weights = _validate_weights(weights, len(checked_values))
    epsilon = float(epsilon)
    if not isfinite(epsilon) or not 0.0 < epsilon < 1.0:
        raise ValueError(f"epsilon must be finite and in (0, 1); got {epsilon!r}")

    if epsilon > 0.5:
        # Identical real-valued equation, evaluated with a cancellation-safe
        # identity near epsilon=1. Let delta=1-epsilon and L be the weighted
        # log product. (exp(L)-epsilon)/delta = 1+expm1(L)/delta, with each
        # log(epsilon+delta*x) = log1p(-delta*(1-x)).
        delta = 1.0 - epsilon
        log_product = sum(
            weight * log1p(-delta * (1.0 - value))
            for value, weight in zip(checked_values, checked_weights)
        )
        result = 1.0 + expm1(log_product) / delta
    else:
        # The direct log-product is stable for small epsilon, including
        # zero-valued inputs where epsilon keeps the logarithm well-defined.
        log_product = sum(
            weight * log(epsilon + (1.0 - epsilon) * value)
            for value, weight in zip(checked_values, checked_weights)
        )
        result = (exp(log_product) - epsilon) / (1.0 - epsilon)
    return _clamp_roundoff(result)


def resilience_projection(
    values: Sequence[float], weights: Sequence[float], epsilon: float
) -> float:
    """Construct a domain-applicable resilience projection R_j."""

    return regularized_geometric(values, weights, epsilon)


def effective_consequence(
    domains: Mapping[str, float],
    weights: Mapping[str, float],
    resilience_applicability: Mapping[str, float],
    domain_resilience: Mapping[str, float],
) -> float:
    """Compute consequence using domain-applicable resilience projections.

    A scalar RRAS remains useful as a reporting aggregate, but the governing hazard
    equation uses the matching ``R_j`` projection for each consequence domain.
    """

    if (
        set(domains) != set(weights)
        or set(domains) != set(resilience_applicability)
        or set(domains) != set(domain_resilience)
    ):
        raise ValueError(
            "domains, weights, resilience_applicability, and domain_resilience must share keys"
        )
    keys = tuple(domains)
    domain_weights = _validate_weights(tuple(weights[key] for key in keys), len(keys))
    terms = []
    for key, weight in zip(keys, domain_weights):
        domain_score = _bounded(domains[key], f"domains[{key!r}]")
        applicability = _bounded(
            resilience_applicability[key], f"resilience_applicability[{key!r}]"
        )
        projected_resilience = _bounded(domain_resilience[key], f"domain_resilience[{key!r}]")
        terms.append(weight * domain_score * (1.0 - applicability * projected_resilience))
    return _clamp_roundoff(sum(terms))


def hazard_pressure(te: float, d_eff: float) -> float:
    """Compute H(t) = TE(t) * D_eff(t)."""

    return _bounded(te, "te") * _bounded(d_eff, "d_eff")


def mitigation(soe: float, cm: float, m0: float) -> float:
    """Compute M(t) = SOE(t) * [m0 + (1-m0) * CM(t)]."""

    checked_soe = _bounded(soe, "soe")
    checked_cm = _bounded(cm, "cm")
    checked_m0 = _bounded(m0, "m0")
    return _clamp_roundoff(checked_soe * (checked_m0 + (1.0 - checked_m0) * checked_cm))


def instantaneous_residual(hazard: float, effective_mitigation: float) -> float:
    """Compute R_inst(t) = H(t) * [1 - M(t)]."""

    return _bounded(hazard, "hazard") * (1.0 - _bounded(effective_mitigation, "mitigation"))


def update_persistent_stock(
    stock: float,
    residual: float,
    effective_mitigation: float,
    beta: float,
    kappa: float,
    dt: float,
) -> float:
    """Apply the exact piecewise-constant stock-flow update from the paper.

    The update is cadence-aware: beta and kappa are rates in the declared time unit,
    while dt is the elapsed interval in that same unit.
    """

    checked_stock = _bounded(stock, "stock")
    checked_residual = _bounded(residual, "residual")
    checked_mitigation = _bounded(effective_mitigation, "mitigation")
    beta = _nonnegative_rate(beta, "beta")
    kappa = _nonnegative_rate(kappa, "kappa")
    dt = float(dt)
    if not isfinite(dt) or dt < 0.0:
        raise ValueError(f"dt must be finite and non-negative; got {dt!r}")

    q = beta * checked_residual + kappa * checked_mitigation
    # Finite individual rates can overflow when added. Never return a
    # seemingly valid but mathematically wrong equilibrium from q = +inf.
    if not isfinite(q):
        raise ValueError("combined stock-flow rate must remain finite")
    if q == 0.0 or dt == 0.0:
        return checked_stock
    steady_state = beta * checked_residual / q
    result = steady_state + (checked_stock - steady_state) * exp(-q * dt)
    return _clamp_roundoff(result)


@dataclass(frozen=True)
class CRPIResult:
    """Decomposed state for one reporting interval."""

    t: float
    te: float
    cs: float
    rras: float
    resilience_by_domain: Mapping[str, float]
    cm: float
    soe: float
    d_eff: float
    hazard: float
    mitigation: float
    residual: float
    stock: float
    crpi: float

    @property
    def usom(self) -> float:
        """Read-only historical alias for the v0.1 result field; use ``soe``."""
        return self.soe

    def as_dict(self) -> dict[str, object]:
        """Return a CSV/JSON-friendly representation."""

        return asdict(self)


def evaluate_step(
    *,
    t: float,
    te: float,
    consequence_domains: Mapping[str, float],
    consequence_weights: Mapping[str, float],
    resilience_applicability: Mapping[str, float],
    domain_resilience: Mapping[str, float],
    rras: float,
    cm: float,
    soe: float,
    m0: float,
    stock: float,
    beta: float,
    kappa: float,
    dt: float,
) -> CRPIResult:
    """Evaluate one CRPI interval with a supplied prior persistent stock."""

    checked_te = _bounded(te, "te")
    checked_rras = _bounded(rras, "rras")
    checked_cm = _bounded(cm, "cm")
    checked_soe = _bounded(soe, "soe")
    d_eff = effective_consequence(
        consequence_domains,
        consequence_weights,
        resilience_applicability,
        domain_resilience,
    )
    cs = weighted_sum(
        tuple(consequence_domains[key] for key in consequence_weights),
        tuple(consequence_weights[key] for key in consequence_weights),
    )
    hazard = hazard_pressure(checked_te, d_eff)
    effective_mitigation = mitigation(checked_soe, checked_cm, m0)
    residual = instantaneous_residual(hazard, effective_mitigation)
    checked_stock = _bounded(stock, "stock")
    persistent = update_persistent_stock(
        checked_stock, residual, effective_mitigation, beta, kappa, dt
    )
    return CRPIResult(
        t=float(t),
        te=checked_te,
        cs=cs,
        rras=checked_rras,
        resilience_by_domain=dict(domain_resilience),
        cm=checked_cm,
        soe=checked_soe,
        d_eff=d_eff,
        hazard=hazard,
        mitigation=effective_mitigation,
        residual=residual,
        stock=persistent,
        crpi=max(residual, persistent),
    )


def simulate(
    rows: Iterable[Mapping[str, object]],
    *,
    consequence_weights: Mapping[str, float],
    resilience_applicability: Mapping[str, float],
    m0: float,
    beta: float,
    kappa: float,
    dt: float,
    initial_stock: float | None = None,
) -> list[CRPIResult]:
    """Evaluate ordered inputs, carrying persistent exposure between rows.

    Each row must contain ``t``, ``te``, ``consequence_domains``, ``rras``, ``cm``,
    and ``soe`` plus ``domain_resilience``. The first row uses the supplied initial stock, or the bounded
    state-neutral paper default ``S(t0) = R_inst(t0)``. Subsequent rows use the current interval's
    residual and mitigation in the exact update, matching the worked example's
    reporting convention.
    """

    materialized = list(rows)
    # Historical in-memory rows may still have the v0.1 key; never let
    # conflicting aliases choose a value silently.
    for row in materialized:
        if "soe" in row and "usom" in row:
            raise ValueError("provide either soe or historical usom, not both")
    if not materialized:
        return []

    results: list[CRPIResult] = []
    previous_stock: float | None = initial_stock
    for index, row in enumerate(materialized):
        provisional = evaluate_step(
            t=float(row["t"]),
            te=float(row["te"]),
            consequence_domains=row["consequence_domains"],  # type: ignore[arg-type]
            consequence_weights=consequence_weights,
            resilience_applicability=resilience_applicability,
            domain_resilience=row["domain_resilience"],  # type: ignore[arg-type]
            rras=float(row["rras"]),
            cm=float(row["cm"]),
            soe=float(row["soe"] if "soe" in row else row["usom"]),
            m0=m0,
            stock=previous_stock if previous_stock is not None else 0.0,
            beta=beta,
            kappa=kappa,
            dt=0.0,
        )
        if index == 0 and previous_stock is None:
            current_stock = provisional.residual
        else:
            current_stock = update_persistent_stock(
                previous_stock if previous_stock is not None else provisional.residual,
                provisional.residual,
                provisional.mitigation,
                beta,
                kappa,
                dt,
            )
        result = CRPIResult(
            **{
                **provisional.as_dict(),
                "stock": current_stock,
                "crpi": max(provisional.residual, current_stock),
            }
        )
        results.append(result)
        previous_stock = current_stock
    return results
