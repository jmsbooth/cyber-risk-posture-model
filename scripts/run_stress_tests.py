"""Deterministic, nonempirical CRPI operational stress tests.

Uses only the standard library and the existing models.crm_reference module.
Fixed seed and the checked-in illustrative-v0.1 profile govern all examples.
Synthetic draws test mathematical behavior, not empirical security outcomes.

    python scripts/run_stress_tests.py --output verification/stress_test_results.json
    python scripts/run_stress_tests.py --check verification/stress_test_results.json
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import random
import sys
from pathlib import Path
from statistics import mean

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from models.crm_reference import (
    effective_consequence, instantaneous_residual, mitigation,
    regularized_geometric, resilience_projection, update_persistent_stock,
)

PROFILE_PATH = ROOT / 'config/calibration_baseline.json'
SEED = 20261023
N = 12000
DOMAINS = ('confidentiality', 'integrity', 'availability')
FIELDS = (
    'TE_external', 'TE_internal', 'CS_confidentiality', 'CS_integrity',
    'CS_availability', 'CM_coverage', 'CM_freshness', 'CM_integrity',
    'CM_verification', 'USOM_detection', 'USOM_velocity',
    'USOM_change_safety', 'USOM_learning', 'RRAS_internal',
    'RRAS_dependency',
)
THREAT = {'TE_external', 'TE_internal', 'CS_confidentiality',
          'CS_integrity', 'CS_availability'}
CAPABILITY = set(FIELDS) - THREAT
THRESHOLD = 0.15  # illustrative classification threshold, NOT calibrated action policy


def quantile(data: list[float], p: float) -> float:
    if not data:
        raise ValueError('quantile of empty dataset')
    xs = sorted(data)
    j = p * (len(xs)-1)
    lo = int(j)
    return xs[lo] + (xs[min(lo+1, len(xs)-1)]-xs[lo])*(j-lo)


def score(fields: dict[str, float], profile: dict) -> dict[str, float]:
    """Use published normalization, domain projection, and CRPI equations."""
    w = profile['weights']
    te = regularized_geometric([fields['TE_external'], fields['TE_internal']],
                               w['te'], profile['epsilon_te'])
    rp = [fields['RRAS_internal'], fields['RRAS_dependency']]
    resilience = {d: resilience_projection(rp, w['rras']['by_domain'][d],
                    profile['epsilon_r']) for d in DOMAINS}
    domains = {d: fields[f'CS_{d}'] for d in DOMAINS}
    consequence = effective_consequence(domains, w['consequence'],
                         profile['resilience_applicability'], resilience)
    cm = mean(fields[f'CM_{k}'] for k in ('coverage','freshness','integrity','verification'))
    usom = mean(fields[f'USOM_{k}'] for k in ('detection','velocity','change_safety','learning'))
    m = mitigation(usom, cm, profile['m0'])
    residual = instantaneous_residual(te * consequence, m)
    return {'te':te, 'd_eff':consequence, 'cm':cm, 'usom':usom,
            'mitigation':m, 'residual':residual,
            'rras_reporting':regularized_geometric(rp,w['rras']['reporting'],
                                                    profile['epsilon_rras']),
            **{f'r_{d}': resilience[d] for d in DOMAINS}}


def generate(rng: random.Random) -> dict[str,float]:
    return {key: rng.betavariate(2.0,2.0) for key in FIELDS}


def mask_one(x: dict[str,float], rng: random.Random, kind: str) -> set[str]:
    if kind=='mcar_10':
        return {k for k in FIELDS if rng.random()<.10}
    if kind=='mcar_20':
        return {k for k in FIELDS if rng.random()<.20}
    if kind=='risk_correlated':
        masks={k for k in FIELDS if rng.random()<.04}
        if x['TE_external']>.7 and rng.random()<.80:
            masks.add('TE_external')
        if x['CS_availability']>.75 and rng.random()<.70:
            masks.add('CS_availability')
        if x['USOM_detection']<.3 and rng.random()<.80:
            masks.add('USOM_detection')
        return masks
    raise ValueError(kind)


def fillings(x: dict[str,float], masked: set[str]) -> tuple[dict,dict,dict]:
    neutral=x.copy()
    lower=x.copy()
    upper=x.copy()
    for key in masked:
        neutral[key]=.5
        lower[key]=0. if key in THREAT else 1.
        upper[key]=1. if key in THREAT else 0.
    return neutral,lower,upper


def missing_stress(rows: list[dict[str,float]],profile:dict,kind:str,seed:int)->dict:
    rng = random.Random(seed)
    widths=[]
    errs=[]
    under=0
    risk_positive=0
    misclassified=0
    threshold_crossing=0
    all_observed=0
    covered=0
    meets_profile_aggregate=0
    for x in rows:
        masked=mask_one(x,rng,kind)
        neutral,lower,upper=fillings(x,masked)
        truth=score(x,profile)['residual']
        guessed=score(neutral,profile)['residual']
        lo=score(lower,profile)['residual']
        hi=score(upper,profile)['residual']
        assert -1e-10<=lo<=truth+1e-10 and truth<=hi+1e-10 and hi<=1+1e-10,(kind,lo,truth,hi)
        widths.append(hi-lo)
        errs.append(guessed-truth)
        covered+=1-len(masked)/len(FIELDS)
        all_observed+=not masked
        meets_profile_aggregate+=(len(masked)<=4) # 11/15 approx >=0.7; not real Tier2 coverage
        risk_positive+=truth>=THRESHOLD
        under+=(guessed<THRESHOLD and truth>=THRESHOLD)
        misclassified+=(guessed>=THRESHOLD and truth<THRESHOLD)
        threshold_crossing+=(lo<THRESHOLD<=hi)
    return {'mechanism':kind,'n':len(rows),
        'observed_fraction_mean':covered/len(rows),
        'full_input_fraction':all_observed/len(rows),
        'raw_fraction_at_least_11_of_15':meets_profile_aggregate/len(rows),
        'interval_width_median':quantile(widths,.5),
        'interval_width_p90':quantile(widths,.9),
        'illustrative_threshold':THRESHOLD,
        'interval_crosses_threshold_fraction':threshold_crossing/len(rows),
        'neutral_imputation_mae':mean(abs(v) for v in errs),
        'neutral_imputation_signed_bias':mean(errs),
        'false_reassurance_fraction_all_rows':under/len(rows),
        'false_reassurance_fraction_true_above_threshold':under/risk_positive if risk_positive else None,
        'false_alarm_fraction_all_rows':misclassified/len(rows),
        'true_above_threshold_fraction':risk_positive/len(rows)}


def quantize_output(x):
    """Keep the archived report compact and deterministic without masking meaning."""
    if isinstance(x,float):
        return round(x,9)
    if isinstance(x,dict):
        return {k:quantize_output(v) for k,v in x.items()}
    if isinstance(x,list):
        return [quantize_output(v) for v in x]
    return x


def cadence(profile:dict)->dict:
    beta,kappa=profile['beta'],profile['kappa']
    initial=.30
    day_hi=(.8,.05)
    day_lo=(.02,.8)
    paths={
        'high_then_recovery':[day_hi]*2+[day_lo]*5,
        'recovery_then_high':[day_lo]*5+[day_hi]*2,
    }
    result={}
    for name,path in paths.items():
        stock=initial
        for resid,m in path:
            stock=update_persistent_stock(stock,resid,m,beta,kappa,1.)
        result[name]=stock
    mean_r=(day_hi[0]*2+day_lo[0]*5)/7
    mean_m=(day_hi[1]*2+day_lo[1]*5)/7
    weekly=update_persistent_stock(initial,mean_r,mean_m,beta,kappa,7.)
    static_full=update_persistent_stock(.2,.35,.4,beta,kappa,7.)
    static_part=.2
    for _ in range(7):
        static_part=update_persistent_stock(static_part,.35,.4,beta,kappa,1.)
    return {'initial_stock':initial,'day_count':7,'input_sequence':{'high':[.8,.05], 'low':[.02,.8], 'n_high':2,'n_low':5},
            'final_stock_high_then_recovery':result['high_then_recovery'],
            'final_stock_recovery_then_high':result['recovery_then_high'],
            'final_stock_coarse_weekly_means':weekly,
            'order_spread':abs(result['high_then_recovery']-result['recovery_then_high']),
            'coarse_max_absolute_error':max(abs(weekly-v) for v in result.values()),
            'static_input_semigroup_difference':abs(static_full-static_part)}


def profile_rank_reversals(rows:list[dict], profile:dict)->dict:
    shifted=copy.deepcopy(profile)
    shifted['weights']['consequence']={'confidentiality':.6,'integrity':.2,'availability':.2}
    # Deterministic independent pair comparison of rankings under alternative governed weights.
    reversals=0
    diffs=[]
    for x,y in zip(rows[0::2],rows[1::2]):
        a,b=score(x,profile)['residual'],score(y,profile)['residual']
        c,d=score(x,shifted)['residual'],score(y,shifted)['residual']
        if (a-b)*(c-d)<0:
            reversals+=1
        diffs.extend([abs(a-c),abs(b-d)])
    return {'baseline_weights':profile['weights']['consequence'],
            'alternative_weights':shifted['weights']['consequence'],
            'pair_count':len(rows)//2,
            'ranking_flip_fraction':reversals/(len(rows)//2),
            'individual_absolute_change_median':quantile(diffs,.5),
            'individual_absolute_change_p90':quantile(diffs,.9)}


def fixed_stresses(profile:dict)->dict:
    geom={str(e):regularized_geometric([0.,.8],[.5,.5],e) for e in (.001,.05,.25,.9,.9999999999999999)}
    beta,kappa=profile['beta'],profile['kappa']
    stock_init=.85
    r,m=.05,.2
    def after(stock,days):
        return update_persistent_stock(stock,r,m,beta,kappa,float(days))
    cold_start=r
    high_stock={'prior_stock_assumed':cold_start,'prior_stock_history':stock_init,
        'day0_crpi_assumed':max(r,cold_start),'day0_crpi_history':max(r,stock_init),
        'day1_crpi_assumed':max(r,after(cold_start,1)),
        'day1_crpi_history':max(r,after(stock_init,1)),
        'day7_crpi_assumed':max(r,after(cold_start,7)),
        'day7_crpi_history':max(r,after(stock_init,7))}
    masked_stock={}
    for resid in (.1,.3):
        s=update_persistent_stock(.90,resid,.6,beta,kappa,1.)
        masked_stock[f'residual_{resid}']={'next_stock':s,'crpi':max(resid,s)}
    diverse_mechanisms={
        'low_hazard_low_mitigation':{'hazard':.4,'mitigation':.5,'residual':.2},
        'high_hazard_high_mitigation':{'hazard':.8,'mitigation':.75,'residual':.2},
    }
    for rec in diverse_mechanisms.values():
        rec['next_stock_from_point_three']=update_persistent_stock(.3,rec['residual'],rec['mitigation'],beta,kappa,1.)
    return {'regularizer_weak_link':geom,'time_order_and_cadence':cadence(profile),
        'unknown_stock_initialization':high_stock,
        'envelope_branch_masking':masked_stock,
        'nonidentifiable_residual_example':diverse_mechanisms}


def run() -> dict:
    # Read as text to normalize LF/CRLF. The archived digest describes the
    # calibration contents, not platform-specific checkout line endings.
    profile_text=PROFILE_PATH.read_text(encoding='utf-8')
    profile=json.loads(profile_text)
    if profile['profile_id']!='illustrative-v0.1':
        raise ValueError('Never silently change calibration scenario profile')
    rng=random.Random(SEED)
    rows=[generate(rng) for _ in range(N)]
    scores=[score(x,profile) for x in rows]
    residuals=[rec['residual'] for rec in scores]
    assert all(0<=v<=1 for v in residuals)
    random_stock=[rng.random() for _ in range(N)]
    risk_from_stock=[update_persistent_stock(s0,v,rec['mitigation'],profile['beta'],profile['kappa'],profile['dt']) for s0,v,rec in zip(random_stock,residuals,scores)]
    crpi=[max(a,b) for a,b in zip(residuals,risk_from_stock)]
    assert all(0<=v<=1 for v in crpi)
    report={
      'schema':'crpi-synthetic-stress-v1', 'profile_id':profile['profile_id'],
      'profile_sha256':hashlib.sha256(profile_text.encode('utf-8')).hexdigest(),
      'seed':SEED, 'base_draws':N,'raw_primitives':list(FIELDS),
      'synthetic_sampling': 'independent Beta(2,2) draws for normalized primitives; independent Uniform(0,1) initial stocks; not representative of organizations',
      'core':{
        'residual_median':quantile(residuals,.5),'residual_p90':quantile(residuals,.9),
        'envelope_median':quantile(crpi,.5),'envelope_p90':quantile(crpi,.9),
        'stock_dominates_one_step_fraction':sum(s>r for s,r in zip(risk_from_stock,residuals))/N,
        'boundedness_violations':sum(not (0<=v<=1) for v in crpi)
      },
      'missingness':{kind:missing_stress(rows,profile,kind,SEED+offset) for offset,kind in enumerate(('mcar_10','mcar_20','risk_correlated'),start=1)},
      'weight_variation':profile_rank_reversals(rows,profile),
      'fixed':fixed_stresses(profile),
      'inference_bound_note':'For missing normalized primitive scores, lower/upper residual bounds substitute 0/1 in the direction implied by monotonicity. These are feasible worst-case mathematical envelopes under independent [0,1] ranges, not confidence intervals or fitted probabilities.',
      'scope':'Uncalibrated synthetic stress tests; outputs characterize formula and missingness-policy behavior only; no predictions or real-world incident labels.'
    }
    return quantize_output(report)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    g=parser.add_mutually_exclusive_group(required=True)
    g.add_argument('--output',type=Path)
    g.add_argument('--check',type=Path)
    args=parser.parse_args()
    result=run()
    rendered=json.dumps(result,sort_keys=True,indent=2)+'\n'
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(rendered,encoding='utf-8')
        print('Wrote',args.output)
    else:
        saved=args.check.read_text(encoding='utf-8')
        if saved!=rendered:
            raise SystemExit('Reproducibility FAIL: stored JSON does not match rerun')
        print('Reproducibility PASS:',args.check)
    print(json.dumps({'draws':N,'summary':result['core'],'missingness':result['missingness'],'weight_variation':result['weight_variation'],'temporal':result['fixed']['time_order_and_cadence']},indent=2))


if __name__=='__main__':
    main()
