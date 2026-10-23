"""Run a CRPI raw-evidence pilot case without altering the governing equations.

Example: python scripts/run_operational_pilot.py --input data/examples/operational_pilot_case.json
All input fields are synthetic/self-attested; results are NOT empirical validation.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0,str(ROOT))
from models.operational_pilot import evaluate


def run(input_path:Path, spec_path:Path, model_path:Path)->dict:
    def read(p):
        return json.loads(p.read_text(encoding='utf-8'))
    return evaluate(read(input_path),read(spec_path),read(model_path))


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input',type=Path,default=ROOT/'data/examples/operational_pilot_case.json')
    parser.add_argument('--measurement-profile',type=Path,default=ROOT/'config/measurement_pilot_v0.1.json')
    parser.add_argument('--model-profile',type=Path,default=ROOT/'config/calibration_baseline.json')
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    out=run(args.input,args.measurement_profile,args.model_profile)
    text=json.dumps(out,indent=2,sort_keys=True,allow_nan=False)+'\n'
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(text,encoding='utf-8')
    print(text,end='')


if __name__=='__main__':
    main()