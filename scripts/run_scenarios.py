"""Run the synthetic CRPI scenarios and write decomposed outputs."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from statistics import mean
from typing import Any

# Support both ``python -m scripts.run_scenarios`` and direct invocation from the
# repository root without requiring an editable package install.
REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from models.crm_reference import regularized_geometric, resilience_projection, simulate
from models.validation import summarize


CM_COLUMNS = ("CM_coverage", "CM_freshness", "CM_integrity", "CM_verification")
SOE_COLUMNS = ("SOE_detection", "SOE_velocity", "SOE_change_safety", "SOE_learning")
CONSEQUENCE_KEYS = ("confidentiality", "integrity", "availability")
DOMAIN_COVERAGE_COLUMNS = tuple(
    f"coverage_{family}_{domain}"
    for family in ("D", "R")
    for domain in CONSEQUENCE_KEYS
)


def _canonical_row(row: dict[str, str]) -> dict[str, str]:
    """Accept historical v0.1 CSV input names without emitting legacy output."""
    current: dict[str, str] = {}
    for key, value in row.items():
        mapped = 'SOE_' + key[5:] if key.startswith('USOM_') else (
            'coverage_SOE' if key == 'coverage_USOM' else key
        )
        if mapped in current:
            raise ValueError(f'conflicting SOE/legacy USOM CSV columns: {mapped}')
        current[mapped] = value
    return current


def _profile(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def _coverage(row: dict[str, str]) -> tuple[float, float, float]:
    tier2_values = [
        float(row[f"coverage_{key}"]) for key in ("CM", "CS", "TE", "SOE", "RRAS")
    ]
    domain_values = [float(row[column]) for column in DOMAIN_COVERAGE_COLUMNS]
    governing_path_values = [
        float(row[f"coverage_{key}"]) for key in ("CM", "TE", "SOE")
    ] + domain_values
    return mean(tier2_values), min(tier2_values), min(governing_path_values)


def _prepared_row(row: dict[str, str], profile: dict[str, Any]) -> dict[str, Any]:
    te = regularized_geometric(
        [float(row["TE_external"]), float(row["TE_internal"])],
        profile["weights"]["te"],
        profile["epsilon_te"],
    )
    rras = regularized_geometric(
        [float(row["RRAS_internal"]), float(row["RRAS_dependency"])],
        profile["weights"]["rras"]["reporting"],
        profile["epsilon_rras"],
    )
    rras_primitives = [float(row["RRAS_internal"]), float(row["RRAS_dependency"])]
    resilience_by_domain = {
        key: resilience_projection(
            rras_primitives,
            profile["weights"]["rras"]["by_domain"][key],
            profile["epsilon_r"],
        )
        for key in CONSEQUENCE_KEYS
    }
    consequence_domains = {
        key: float(row[f"CS_{key}"]) for key in CONSEQUENCE_KEYS
    }
    cm = sum(float(row[column]) for column in CM_COLUMNS) / len(CM_COLUMNS)
    soe = sum(float(row[column]) for column in SOE_COLUMNS) / len(SOE_COLUMNS)
    coverage_mean, coverage_min, coverage_gov = _coverage(row)
    return {
        "t": float(row["t"]),
        "te": te,
        "consequence_domains": consequence_domains,
        "rras": rras,
        "domain_resilience": resilience_by_domain,
        "cm": cm,
        "soe": soe,
        "coverage_mean": coverage_mean,
        "coverage_min": coverage_min,
        "coverage_gov": coverage_gov,
    }


def run(input_path: Path, profile_path: Path, output_dir: Path) -> dict[str, Any]:
    profile = _profile(profile_path)
    grouped: dict[str, list[dict[str, Any]]] = {}
    with input_path.open(newline="", encoding="utf-8") as handle:
        for raw in csv.DictReader(handle):
            raw = _canonical_row(raw)
            grouped.setdefault(raw["scenario"], []).append(_prepared_row(raw, profile))

    consequence_weights = profile["weights"]["consequence"]
    results: list[dict[str, Any]] = []
    summary: dict[str, Any] = {}
    for scenario, rows in grouped.items():
        model_rows = [
            {
                key: value
                for key, value in row.items()
                if key in {"t", "te", "consequence_domains", "rras", "domain_resilience", "cm", "soe"}
            }
            for row in rows
        ]
        evaluated = simulate(
            model_rows,
            consequence_weights=consequence_weights,
            resilience_applicability=profile["resilience_applicability"],
            m0=profile["m0"],
            beta=profile["beta"],
            kappa=profile["kappa"],
            dt=profile["dt"],
        )
        scenario_results = []
        for source_row, result in zip(rows, evaluated):
            output = result.as_dict()
            output.update(
                {
                    "scenario": scenario,
                    "coverage_mean": source_row["coverage_mean"],
                    "coverage_min": source_row["coverage_min"],
                    "coverage_gov": source_row["coverage_gov"],
                    "coverage_qualification": (
                        "qualified"
                        if source_row["coverage_mean"] >= profile["coverage_gates"]["aggregate_min"]
                        and source_row["coverage_min"] >= profile["coverage_gates"]["construct_min"]
                        and source_row["coverage_gov"] >= profile["coverage_gates"]["governing_path_min"]
                        else "restricted"
                    ),
                }
            )
            scenario_results.append(output)
            results.append(output)
        crpi_values = [row["crpi"] for row in scenario_results]
        summary[scenario] = {
            **summarize(crpi_values),
            "initial_crpi": crpi_values[0],
            "final_crpi": crpi_values[-1],
            "final_coverage_mean": scenario_results[-1]["coverage_mean"],
            "final_coverage_min": scenario_results[-1]["coverage_min"],
            "final_coverage_gov": scenario_results[-1]["coverage_gov"],
            "final_coverage_qualification": scenario_results[-1]["coverage_qualification"],
        }

    output_dir.mkdir(parents=True, exist_ok=True)
    output_columns = [
        "scenario", "t", "te", "cs", "rras", "cm", "soe", "d_eff", "hazard",
        "mitigation", "residual", "stock", "crpi", "r_confidentiality", "r_integrity",
        "r_availability", "coverage_mean", "coverage_min", "coverage_gov",
        "coverage_qualification",
    ]
    with (output_dir / "example_results.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=output_columns)
        writer.writeheader()
        writer.writerows(
            {
                **{key: row[key] for key in output_columns if key in row},
                "r_confidentiality": row["resilience_by_domain"]["confidentiality"],
                "r_integrity": row["resilience_by_domain"]["integrity"],
                "r_availability": row["resilience_by_domain"]["availability"],
            }
            for row in results
        )
    report = {
        "profile_id": profile["profile_id"],
        "input": str(input_path),
        "rows": len(results),
        "scenarios": summary,
    }
    with (output_dir / "example_summary.json").open("w", encoding="utf-8") as handle:
        json.dump(report, handle, indent=2)
        handle.write("\n")
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=Path("data/examples/scenarios_soe.csv"))
    parser.add_argument("--profile", type=Path, default=Path("config/calibration_baseline.json"))
    parser.add_argument("--output-dir", type=Path, default=Path("artifacts"))
    args = parser.parse_args()
    report = run(args.input, args.profile, args.output_dir)
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
