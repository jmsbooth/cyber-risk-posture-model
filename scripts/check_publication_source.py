"""Fail-closed source and naming checks for the CRPI review manuscript."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
source = (ROOT / "paper/CRM_revised.tex").read_text(encoding="utf-8")
assert "USOM" not in source and "usom" not in source, "legacy acronym remains in manuscript"
assert r"\date{\today}" not in source, "unstable publication date"
assert "SOE(t)" in source and "Security Operations Effectiveness" in source

order = (
    r"\section{Conceptual Architecture of CRPI}",
    r"\section{Tier~2 Risk Dimensions}",
    r"\section{Measurement Specification}",
    r"\section{Temporal Behavior and Calibration}",
    r"\section{Governing Model}",
    r"\section{Interpreting CRPI Outputs}",
    r"\section{Worked Example}",
    r"\section{Organizational Implementation and Empirical Backtesting}",
)
indices = [source.index(heading) for heading in order]
assert indices == sorted(indices), "narrative section order regressed"
assert source.count(r"\appendix") == 1
assert "Table~" in source and r"\label{tab:primitive-contract}" in source

bib = re.findall(r"\\bibitem\{([^{}]+)\}", source)
cited = [k.strip() for group in re.findall(r"\\cite\{([^{}]+)\}", source) for k in group.split(",")]
labels = re.findall(r"\\label\{([^{}]+)\}", source)
refs = re.findall(r"\\(?:eqref|ref)\{([^{}]+)\}", source)
assert len(bib) == len(set(bib)) and set(cited) <= set(bib)
assert len(labels) == len(set(labels)) and set(refs) <= set(labels)
assert len(bib) >= 30

new = json.loads((ROOT / "config/measurement_pilot_soe_v0.2.json").read_text(encoding="utf-8"))
old = json.loads((ROOT / "config/measurement_pilot_v0.1.json").read_text(encoding="utf-8"))
cal = json.loads((ROOT / "config/calibration_soe_v0.2.json").read_text(encoding="utf-8"))
assert new["score_profile"] == cal["profile_id"]
assert len(new["fields"]) == 15 and len(old["fields"]) == 15
assert len([k for k in new["fields"] if k.startswith("SOE_")]) == 4
assert not any(k.startswith("USOM_") for k in new["fields"])
assert "soe_alpha" in cal["smoothing"] and "usom_alpha" not in cal["smoothing"]
from models.operational_pilot import ALL
assert set(new["fields"]) == set(ALL)

print(f"Source integrity PASS: {len(bib)} references, {len(labels)} labels, {len(order)} ordered sections, 15 canonical SOE primitives")
