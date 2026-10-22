"""Independently regenerate/check Phase D CRPI decimal vectors.

Uses only stdlib Decimal (70 significant digits) and the manuscript equations.
Never imports or invokes models.crm_reference; intentionally not an oracle for
floating-point implementation guarantees or empirical calibration.

Usage:
  python scripts/regenerate_phase_d.py --check
  python scripts/regenerate_phase_d.py --write
"""
from __future__ import annotations

import argparse
import json
from decimal import Decimal, localcontext
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VECTOR_PATH = ROOT / "verification" / "reference_vectors.json"
PLACES = Decimal("0.00000000000000000000000000000001")


def dec(value: object) -> Decimal:
    return Decimal(str(value))


def decimal_string(value: Decimal) -> str:
    return format(value.quantize(PLACES), "f")


def regularized(values: list[str], weights: list[str], epsilon: str) -> Decimal:
    x = [dec(value) for value in values]
    w = [dec(weight) for weight in weights]
    e = dec(epsilon)
    if len(x) != len(w) or not x or not 0 < e < 1:
        raise ValueError("invalid independent oracle input")
    if any(v < 0 or v > 1 for v in x) or any(weight < 0 for weight in w):
        raise ValueError("bounded domain required")
    if abs(sum(w) - 1) > dec("0.000000000000001"):
        raise ValueError("normalized weights required")
    if all(v == 0 for v in x):
        return Decimal(0)
    if all(v == 1 for v in x):
        return Decimal(1)
    exponent = sum((wi * (e + (1 - e) * value).ln()
                    for value, wi in zip(x, w)), Decimal(0))
    return (exponent.exp() - e) / (1 - e)


def step(stock: object, residual: object, mitigation: object,
         beta: object, kappa: object, dt: object) -> tuple[Decimal, Decimal, Decimal | None]:
    q = dec(beta) * dec(residual) + dec(kappa) * dec(mitigation)
    if q == 0:
        return dec(stock), q, None
    equilibrium = dec(beta) * dec(residual) / q
    return equilibrium + (dec(stock) - equilibrium) * (-q * dec(dt)).exp(), q, equilibrium


def compute_worked(inputs: dict[str, object]) -> dict[str, Decimal]:
    te = regularized(inputs["te_values"], inputs["te_weights"], inputs["epsilon_te"])
    dom, w = inputs["consequence_domains"], inputs["consequence_weights"]
    rho, resil = inputs["resilience_applicability"], inputs["domain_resilience"]
    cs = sum((dec(w[key]) * dec(dom[key]) for key in dom), Decimal(0))
    d_eff = sum((dec(w[key]) * dec(dom[key]) * (1 - dec(rho[key]) * dec(resil[key]))
                 for key in dom), Decimal(0))
    hazard = te * d_eff
    mit = dec(inputs["usom"]) * (dec(inputs["m0"]) +
                                        (1 - dec(inputs["m0"])) * dec(inputs["cm"]))
    residual = hazard * (1 - mit)
    stock, q, equilibrium = step(inputs["stock_prev"], residual, mit,
                                  inputs["beta"], inputs["kappa"], inputs["dt"])
    if equilibrium is None:
        raise ValueError("worked example must have positive total rate")
    return {"te": te, "cs": cs, "d_eff": d_eff, "hazard": hazard,
            "mitigation": mit, "residual": residual, "q": q,
            "stock_equilibrium": equilibrium, "stock": stock,
            "crpi": max(stock, residual)}


def run(write: bool) -> None:
    with localcontext() as context:
        context.prec = 70
        document = json.loads(VECTOR_PATH.read_text(encoding="utf-8"))
        assert document["schema_version"] == "crpi-phase-d-v1"
        updates = 0
        for vector in document["aggregation"]:
            got = decimal_string(regularized(vector["values"], vector["weights"], vector["epsilon"]))
            if not write and got != vector["expected"]:
                raise AssertionError(f"aggregate {vector['id']} changed: {got} != {vector['expected']}")
            vector["expected"] = got
            updates += 1
        worked = document["worked_example"]
        for key, value in compute_worked(worked["inputs"]).items():
            got = decimal_string(value)
            if not write and got != worked["expected"][key]:
                raise AssertionError(f"worked.{key} changed: {got} != {worked['expected'][key]}")
            worked["expected"][key] = got
            updates += 1
        for vector in document["persistence"]:
            st, q, eq = step(vector["stock"], vector["residual"], vector["mitigation"],
                             vector["beta"], vector["kappa"], vector["dt"])
            vals = {"expected_stock": decimal_string(st), "expected_q": decimal_string(q),
                    "equilibrium_if_positive_rate": decimal_string(eq) if eq is not None else None}
            for key, got in vals.items():
                if not write and got != vector[key]:
                    raise AssertionError(f"stock {vector['id']}.{key} changed: {got} != {vector[key]}")
                vector[key] = got
                updates += 1
        if write:
            VECTOR_PATH.write_text(json.dumps(document, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
        print(f"Phase D Decimal oracle: {'wrote' if write else 'verified'} {updates} fields")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--write", action="store_true")
    args = parser.parse_args()
    run(write=args.write)
