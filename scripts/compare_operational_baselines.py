"""Structural (NON-EMPIRICAL) baseline comparison for CRPI measurement pilot.

No observed incident outcomes, fitted coefficients or predictive AUC are generated.
The simple additive baseline is intentionally a different construct; compare rank
sensitivity and score decomposition, not forecasting skill or interval calibration.
"""
from __future__ import annotations

import argparse
import copy
import json
import random
import sys
from pathlib import Path
from statistics import mean, median

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0,str(ROOT))
from models.crm_reference import update_persistent_stock
from models.operational_pilot import ALL, TE, _score, evaluate

SEED = 20261023
N=600
PAIRS=5000


def _read(p:Path):
    return json.loads(p.read_text(encoding='utf-8'))


def quantize(x):
    if isinstance(x,float):
        return round(x,9)
    if isinstance(x,dict):
        return {k:quantize(v) for k,v in x.items()}
    if isinstance(x,list):
        return [quantize(v) for v in x]
    return x


def rank_disagreement(model:list[float],comparison:list[float],pairs:list[tuple[int,int]])->dict:
    reversed_count=0
    ties=0
    for i,j in pairs:
        d1=model[i]-model[j]
        d2=comparison[i]-comparison[j]
        if abs(d1)<1e-12 or abs(d2)<1e-12:
            ties+=1
        elif d1*d2<0:
            reversed_count+=1
    effective=len(pairs)-ties
    return {'evaluated_pairs':effective,'excluded_ties':ties,
            'rank_reversal_fraction':reversed_count/effective if effective else None}


def run()->dict:
    base=_read(ROOT/'data/examples/operational_pilot_case.json')
    measure=_read(ROOT/'config/measurement_pilot_v0.1.json')
    profile=_read(ROOT/'config/calibration_baseline.json')
    baseline=evaluate(base,measure,profile)
    if baseline['missing_required']:
        raise AssertionError('pilot demo fixture must contain complete valid evidence')
    shorter=copy.deepcopy(measure)
    shorter['fields']['USOM_velocity']['U']=24.0
    shortened=evaluate(base,shorter,profile)
    changed=copy.deepcopy(base)
    changed['observations']['TE_external']['denominator']=10
    denominator_shift=evaluate(changed,measure,profile)
    missing=copy.deepcopy(base)
    del missing['observations']['TE_external']
    missing_result=evaluate(missing,measure,profile)
    stale=copy.deepcopy(base)
    stale['observations']['USOM_detection']['observed_at']='2026-01-01T00:00:00Z'
    stale_result=evaluate(stale,measure,profile)

    rng=random.Random(SEED)
    scores={'crpi':[],'instantaneous_residual':[],'simple_additive':[],
            'arithmetic_te_ablation':[]}
    for _ in range(N):
        x={k:rng.betavariate(2,2) for k in ALL}
        prior=rng.betavariate(2,2)  # invented prior stock, not observed history
        step=_score(x,profile,prior_stock=prior,dt=1.0)
        residual=step['R_inst']
        te_arithmetic=(x[TE[0]]+x[TE[1]])/2.0
        r_arithmetic=te_arithmetic*step['D_eff']*(1-step['M'])
        s_arithmetic=update_persistent_stock(prior,r_arithmetic,step['M'],
                                               profile['beta'],profile['kappa'],1.0)
        scores['crpi'].append(step['CRPI'])
        scores['instantaneous_residual'].append(residual)
        scores['simple_additive'].append((step['TE']+step['D_eff']+(1-step['M']))/3.)
        scores['arithmetic_te_ablation'].append(max(r_arithmetic,s_arithmetic))
    pair_list=[tuple(rng.sample(range(N),2)) for _ in range(PAIRS)]
    comparisons={}
    for key,values in scores.items():
        comparisons[key]={
          'mean':mean(values),'median':median(values),
          'p05':sorted(values)[int(.05*(N-1))],
          'p95':sorted(values)[int(.95*(N-1))],
        }
        if key!='crpi':
            comparisons[key].update(rank_disagreement(scores['crpi'],values,pair_list))
    return quantize({
        'schema':'crpi-operational-measurement-baseline-structural-v0.1',
        'provenance':{'seed':SEED,'simulated_scopes':N,'comparison_pairs':PAIRS,
                      'synthetic_inputs':'independent Beta(2,2) normalized primitives',
                      'prior_stock':'independent Beta(2,2) synthetic history',
                      'scoring_profile':'illustrative-v0.1',
                      'measurement_profile':'crpi-pilot-measurement-profile-v0.1'},
        'pilot_raw_evidence_sensitivity':{
            'base_residual':baseline['point']['R_inst'],
            'base_crpi':baseline['point']['CRPI'],
            'base_coverage_governing':baseline['coverage']['governing_path_min'],
            'shorter_containment_time_normalization_residual':shortened['point']['R_inst'],
            'shorter_containment_time_normalization_crpi':shortened['point']['CRPI'],
            'reduced_external_denominator_residual':denominator_shift['point']['R_inst'],
            'reduced_external_denominator_crpi':denominator_shift['point']['CRPI'],
            'missing_external_point_is_null':missing_result['point'] is None,
            'missing_external_residual_interval':missing_result['residual_possible_interval'],
            'stale_detection_point_is_null':stale_result['point'] is None,
            'stale_detection_reason':stale_result['evidence']['USOM_detection']['reason'],
            'missing_external_governing_coverage':missing_result['coverage']['governing_path_min'],
        },
        'structural_baselines':comparisons,
        'claim_limits':[
            'All raw evidence and simulated pairs are synthetic; there are no organization-level outcomes.',
            'The additive index aggregates adverse constructs and is not the same physical risk quantity as CRPI.',
            'Rank disagreement is not prediction accuracy, statistical significance or model superiority.',
            'Normalized input cutoffs, governance policies and priors are illustrative, not empirically calibrated.'
        ]
    })


def main()->None:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output',type=Path,default=ROOT/'verification/measurement_pilot_structural_results.json')
    p.add_argument('--check',type=Path,help='require JSON values match a stored reference')
    args=p.parse_args()
    result=run()
    if args.check:
        expected=_read(args.check)
        if expected!=result:
            differing=[key for key in set(expected)|set(result)
                       if expected.get(key)!=result.get(key)]
            raise SystemExit('Pilot reproduction FAIL: '+', '.join(sorted(differing)))
        print('Pilot structural reproduction PASS: '+str(args.check))
    else:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n',encoding='utf-8')
        print(json.dumps(result,indent=2,sort_keys=True))


if __name__=='__main__':
    main()