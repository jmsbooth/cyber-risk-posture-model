"""Local-manual Phase D conformance and Lean audit evidence capture.

Run from repository root: python scripts/capture_phase_d.py
Optionally add --with-tex to attempt a local manuscript PDF build. Nothing is
claimed to pass unless its command exits successfully and its outputs are audited.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import platform
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "formal" / "lean"
CODE = ("models", "tests", "scripts", "config", "formal/lean",
        "paper/CRM_revised.tex", "data/examples/scenarios.csv", "verification/reference_vectors.json")
INPUTS = ("models/crm_reference.py", "models/validation.py", "config/calibration_baseline.json",
          "paper/CRM_revised.tex", "data/examples/scenarios.csv",
          "verification/reference_vectors.json", "scripts/regenerate_phase_d.py",
          "tests/test_phase_d_conformance.py", "formal/lean/lake-manifest.json")
ALLOWED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
EXPECTED_AUDIT_SIZES = {"A": 11, "B": 24, "C": 21}


def execute(argv: list[str], cwd: Path, dest: Path) -> str:
    result = subprocess.run(argv, cwd=cwd, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT, text=True, encoding="utf-8",
                            errors="replace", check=False)
    dest.write_text(result.stdout, encoding="utf-8")
    if result.returncode:
        raise RuntimeError(f"Command failed ({result.returncode}): {argv!r}; log: {dest}")
    return result.stdout


def git(*args: str) -> str:
    p = subprocess.run(["git", *args], cwd=ROOT, capture_output=True,
                       text=True, encoding="utf-8", check=True)
    return p.stdout.strip()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_axioms(name: str, log: str) -> dict[str, object]:
    audit_path = LEAN / "CRPI" / ("Audit.lean" if name == "A" else f"Audit{name}.lean")
    expected = re.findall(r"^#print axioms (CRPI\.\w+)$", audit_path.read_text(encoding="utf-8"), re.M)
    reported = re.findall(r"'(CRPI\.\w+)' depends on axioms: \[([^\]]*)\]", log)
    actual = [theorem for theorem, _ in reported]
    if len(expected) != EXPECTED_AUDIT_SIZES[name] or len(actual) != len(expected):
        raise RuntimeError(f"Phase {name}: incorrect axiom declaration count: {len(actual)}/{len(expected)}")
    if set(expected) != set(actual) or len(set(actual)) != len(actual):
        raise RuntimeError(f"Phase {name}: axiom output has missing/duplicated theorem declarations")
    observed: set[str] = set()
    for theorem, labels in reported:
        axioms = {x.strip() for x in labels.split(",") if x.strip()}
        if not axioms.issubset(ALLOWED_AXIOMS):
            raise RuntimeError(f"Phase {name}: unexpected axiom on {theorem}: {axioms - ALLOWED_AXIOMS}")
        observed |= axioms
    return {"theorem_count": len(expected), "observed_axioms": sorted(observed), "status": "pass"}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--with-tex", action="store_true", help="also run Tectonic PDF build")
    args = parser.parse_args()
    if not shutil.which("git") or not shutil.which("lake"):
        raise SystemExit("Git and Lean/Lake must be installed for full Phase D capture")
    sha = git("rev-parse", "HEAD")
    if not re.fullmatch(r"[a-f0-9]{40}", sha):
        raise SystemExit("Cannot identify the exact source revision")
    dirty = git("status", "--porcelain", "--", *CODE)
    if dirty:
        raise SystemExit(f"Source inputs are uncommitted: \n{dirty}\nCommit before evidence capture.")
    evidence = ROOT / "verification" / "evidence" / sha
    evidence.mkdir(parents=True, exist_ok=True)
    toolchain = (LEAN / "lean-toolchain").read_text(encoding="utf-8").strip()
    mathlib_pin = next(pkg["rev"] for pkg in json.loads((LEAN / "lake-manifest.json").read_text(encoding="utf-8"))["packages"] if pkg["name"] == "mathlib")
    installed_mathlib = subprocess.run(["git", "-C", str(LEAN / ".lake/packages/mathlib"), "rev-parse", "HEAD"],
                                      check=True, capture_output=True, text=True).stdout.strip()
    if installed_mathlib != mathlib_pin:
        raise SystemExit("Installed Mathlib commit does not match frozen manifest")
    version = execute(["lake", "env", "lean", "--version"], LEAN, evidence / "phase-d-lean-version.log").strip()
    match = re.fullmatch(r"leanprover/lean4:v(\d+\.\d+\.\d+)", toolchain)
    if match is None or f"Lean (version {match.group(1)}," not in version:
        raise SystemExit("Effective Lean toolchain does not match pinned project version")

    results: dict[str, object] = {}
    py = sys.executable
    operations = [
        ("decimal_oracle", [py, "scripts/regenerate_phase_d.py", "--check"], ROOT),
        ("python_unittest", [py, "-m", "unittest", "discover", "-v"], ROOT),
        ("invariant_report", [py, "scripts/validate_model.py"], ROOT),
    ]
    for name, command, directory in operations:
        output = execute(command, directory, evidence / f"phase-d-{name}.log")
        results[name] = {"status": "pass", "exit_code": 0, "command": command[1:]}
        if name == "python_unittest":
            match = re.search(r"Ran (\d+) tests in", output)
            if not match or int(match.group(1)) < 10 or "\nOK" not in output:
                raise RuntimeError("Could not confirm complete unittest report")
            results[name]["test_count"] = int(match.group(1))
        if name == "invariant_report":
            report = json.loads(output)
            if report.get("status") != "pass" or not all(check.get("status") == "pass" for check in report["checks"]):
                raise RuntimeError("CRPI invariant report is not a passing result")
            results[name]["check_count"] = len(report["checks"])

    with tempfile.TemporaryDirectory(prefix="crpi-phase-d-") as temporary:
        command = [py, "scripts/run_scenarios.py", "--output-dir", temporary]
        output = execute(command, ROOT, evidence / "phase-d-scenarios.log")
        report = json.loads(output)
        if set(report["scenarios"]) != set(json.loads((ROOT / "verification/reference_vectors.json").read_text(encoding="utf-8"))["readme_scenarios_rounded"]):
            raise RuntimeError("Scenario set differs from declared reference vectors")
        results["scenarios"] = {"status": "pass", "exit_code": 0, "row_count": report["rows"],
                                "scenario_count": len(report["scenarios"])}

    build = execute(["lake", "build"], LEAN, evidence / "phase-d-lean-build.log")
    if "Build completed successfully" not in build:
        raise RuntimeError("No successful Lean build completion marker")
    results["lean_build"] = {"status": "pass", "exit_code": 0}
    for phase in ("A", "B", "C"):
        audit = "Audit.lean" if phase == "A" else f"Audit{phase}.lean"
        output = execute(["lake", "env", "lean", f"CRPI/{audit}"], LEAN,
                         evidence / f"phase-d-axioms-{phase.lower()}.log")
        results[f"lean_axioms_{phase.lower()}"] = check_axioms(phase, output)
    if args.with_tex:
        if not shutil.which("tectonic"):
            results["manuscript_pdf"] = {"status": "not_run", "reason": "tectonic unavailable"}
        else:
            with tempfile.TemporaryDirectory(prefix="crpi-tex-") as temp:
                execute(["tectonic", "--outdir", temp, "paper/CRM_revised.tex"], ROOT,
                        evidence / "phase-d-tectonic.log")
                if not (Path(temp) / "CRM_revised.pdf").exists():
                    raise RuntimeError("Tectonic returned success but manuscript PDF is absent")
            results["manuscript_pdf"] = {"status": "pass", "exit_code": 0}
    else:
        results["manuscript_pdf"] = {"status": "not_run", "reason": "--with-tex not requested"}

    vector_doc = json.loads((ROOT / "verification/reference_vectors.json").read_text(encoding="utf-8"))
    record = {
        "schema": "crpi-phase-d-evidence-v1",
        "source_commit": sha,
        "captured_utc": datetime.now(timezone.utc).isoformat(),
        "platform": platform.platform(),
        "python_version": sys.version.split()[0],
        "lean_version": version,
        "lean_toolchain_pin": toolchain,
        "mathlib_revision": installed_mathlib,
        "input_sha256": {path: sha256(ROOT / path) for path in INPUTS},
        "results": results,
        "tolerances": {key: value for key, value in vector_doc.items()
                       if key in ("absolute_tolerance", "relative_tolerance", "manuscript_rounded_tolerance")},
        "scope": "Numerical conformance under synthetic inputs; not an empirical cyber-risk validation",
        "status": "pass" if all(value["status"] == "pass" for key, value in results.items()
                               if key != "manuscript_pdf") else "partial",
    }
    (evidence / "phase-d-summary.json").write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print(f"Phase D local conformance passed for source: {sha}")
    print(f"Python regression tests: {results['python_unittest']['test_count']}; Lean theorem audits: 56")
    print(f"Evidence: {evidence}")
    print("Commit and push the phase-d evidence files; manuscript PDF is separately qualified.")


if __name__ == "__main__":
    main()
