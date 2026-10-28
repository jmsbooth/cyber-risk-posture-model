"""CRPI pilot measurement adapter; uncalibrated and NOT an empirical validator.

Maps 15 scoped evidence records to the EXISTING CRPI reference equations. Missing,
stale or unverified evidence stays missing. Never equate completeness with confidence.
All raw-unit bounds and ordinal anchors belong to a named, provisional profile.
"""
from __future__ import annotations

from datetime import datetime, timezone
from math import isfinite
from statistics import mean
from typing import Any, Mapping

from models.crm_reference import (
    effective_consequence, hazard_pressure, instantaneous_residual, mitigation,
    regularized_geometric, resilience_projection, update_persistent_stock,
)

TE = ('TE_external', 'TE_internal')
CS = ('CS_confidentiality', 'CS_integrity', 'CS_availability')
CM = ('CM_coverage', 'CM_freshness', 'CM_integrity', 'CM_verification')
SOE = ('SOE_detection', 'SOE_velocity', 'SOE_change_safety', 'SOE_learning')
RRAS = ('RRAS_internal', 'RRAS_dependency')
ALL = TE + CS + CM + SOE + RRAS
GROUPS = {'TE': TE, 'CS': CS, 'CM': CM, 'SOE': SOE, 'RRAS': RRAS}
DOMAINS = ('confidentiality', 'integrity', 'availability')


def _canonical_fields(values: Mapping[str, Any]) -> dict[str, Any]:
    """Migrate v0.1 USOM primitive keys only at the input boundary."""
    result: dict[str, Any] = {}
    for key, value in values.items():
        current = 'SOE_' + key[5:] if key.startswith('USOM_') else key
        if current in result:
            raise ValueError(f'conflicting legacy/canonical names for {current}')
        result[current] = value
    return result


def _time(value: str, field: str) -> datetime:
    if not isinstance(value, str):
        raise ValueError(f'{field}: expected ISO-8601 timestamp')
    try:
        out = datetime.fromisoformat(value.replace('Z', '+00:00'))
    except ValueError as ex:
        raise ValueError(f'{field}: invalid ISO-8601 timestamp') from ex
    if out.tzinfo is None or out.utcoffset() is None:
        raise ValueError(f'{field}: timezone offset required')
    return out.astimezone(timezone.utc)


def _number(value: Any, field: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f'{field}: numeric value required')
    n = float(value)
    if not isfinite(n):
        raise ValueError(f'{field}: finite value required')
    return n


def _integer(value: Any, field: str) -> int:
    n = _number(value, field)
    if not n.is_integer():
        raise ValueError(f'{field}: integer count required')
    return int(n)


def _normalize(record: Mapping[str, Any], spec: Mapping[str, Any], field: str) -> float:
    method = spec['method']
    if method == 'fraction':
        numerator = _integer(record.get('numerator'), field + '.numerator')
        denominator = _integer(record.get('denominator'), field + '.denominator')
        if denominator <= 0 or numerator < 0 or numerator > denominator:
            raise ValueError(f'{field}: numerator/denominator must satisfy 0 <= n <= d, d > 0')
        value = numerator / denominator
    elif method == 'ordinal_five':
        level = _integer(record.get('level'), field + '.level')
        if not 0 <= level <= 4:
            raise ValueError(f'{field}: ordinal level must be an integer 0..4')
        value = level / 4.0
    elif method == 'inverse_bounded_hours':
        hours = _number(record.get('hours'), field + '.hours')
        lower, upper = _number(spec['L'], 'L'), _number(spec['U'], 'U')
        if hours < 0 or lower < 0 or upper <= lower:
            raise ValueError(f'{field}: invalid hours or pilot time bounds')
        value = 1.0 - min(1.0, max(0.0, (hours - lower) / (upper - lower)))
    else:
        raise ValueError(f'{field}: unsupported normalization method {method!r}')
    return value


def _score(values: Mapping[str, float], model: Mapping[str, Any],
           *, prior_stock: float | None = None, dt: float | None = None,
           cold_start: bool = False) -> dict[str, Any]:
    """Compose unchanged canonical model functions from normalized primitives."""
    weights = model['weights']
    te = regularized_geometric([values[k] for k in TE], weights['te'], model['epsilon_te'])
    consequence = {d: values['CS_' + d] for d in DOMAINS}
    projections = {
        d: resilience_projection([values[k] for k in RRAS], weights['rras']['by_domain'][d],
                                 model['epsilon_r']) for d in DOMAINS
    }
    d_eff = effective_consequence(consequence, weights['consequence'],
                                  model['resilience_applicability'], projections)
    cs_report = sum(weights['consequence'][d] * consequence[d] for d in DOMAINS)
    rras = regularized_geometric([values[k] for k in RRAS], weights['rras']['reporting'],
                                 model['epsilon_rras'])
    cm, soe = mean(values[k] for k in CM), mean(values[k] for k in SOE)
    h = hazard_pressure(te, d_eff)
    m = mitigation(soe, cm, model['m0'])
    residual = instantaneous_residual(h, m)
    result = {
        'TE': te, 'CS': cs_report, 'CM': cm, 'SOE': soe, 'RRAS_reporting': rras,
        'D_by_domain': consequence, 'R_by_domain': projections,
        'D_eff': d_eff, 'H': h, 'M': m, 'R_inst': residual,
        'S_next': None, 'CRPI': None, 'envelope_branch': None,
        'history_mode': 'not_supplied',
    }
    if prior_stock is not None:
        if cold_start:
            raise ValueError('prior_stock and cold_start cannot be combined')
        if dt is None:
            raise ValueError('dt required when prior_stock is supplied')
        stock = update_persistent_stock(prior_stock, residual, m, model['beta'], model['kappa'], dt)
        result['history_mode'] = 'supplied_prior_stock'
    elif cold_start:
        stock = residual   # t0 is a marked initialization, not an inferred history
        result['history_mode'] = 'declared_cold_start_t0'
    else:
        return result
    result['S_next'] = stock
    result['CRPI'] = max(residual, stock)
    result['envelope_branch'] = ('instantaneous' if residual > stock else
                                 'persistent' if stock > residual else 'tie')
    return result


def evaluate(document: Mapping[str, Any], measurement_profile: Mapping[str, Any],
             model_profile: Mapping[str, Any]) -> dict[str, Any]:
    """Assess the provenance and score only fully observed, freshly attested inputs.

    Incomplete evidence yields admissible residual bounds, never point imputation.
    Coverage reports are completeness fractions, *not* probabilistic confidence.
    """
    if document.get('measurement_profile_id') != measurement_profile.get('schema'):
        raise ValueError('measurement profile id mismatch')
    if document.get('data_class') not in ('synthetic_demo', 'self_reported_pilot'):
        raise ValueError('data_class must explicitly identify synthetic or self-reported pilot evidence')
    scope = document.get('scope_id')
    if not isinstance(scope, str) or not scope.strip():
        raise ValueError('scope_id required')
    as_of = _time(document.get('as_of'), 'as_of')
    if model_profile.get('profile_id') != measurement_profile.get('score_profile'):
        raise ValueError('CRPI calibration profile mismatch')
    defs = _canonical_fields(measurement_profile.get('fields', {}))
    if set(defs) != set(ALL):
        raise ValueError('measurement profile must define exactly 15 known input fields')
    supplied = document.get('observations', {})
    if not isinstance(supplied, dict):
        raise ValueError('observations must be an object')
    supplied = _canonical_fields(supplied)
    if set(supplied) - set(ALL):
        raise ValueError('observations must be an object with only recognized primitive fields')
    values: dict[str, float] = {}
    evidence: dict[str, dict[str, Any]] = {}
    refs: dict[str, list[str]] = {}
    for field in ALL:
        row = supplied.get(field)
        if row is None:
            evidence[field] = {'usable': False, 'reason': 'missing'}
            continue
        if not isinstance(row, dict):
            raise ValueError(f'{field}: observation must be an object')
        age = (as_of - _time(row.get('observed_at'), field + '.observed_at')).total_seconds() / 86400.0
        if age < 0:
            raise ValueError(f'{field}: future-dated evidence is not allowed')
        if row.get('scope_id') != scope:
            raise ValueError(f'{field}: evidence scope_id does not match assessment scope')
        source = row.get('source_ref')
        evidence_id = row.get('evidence_id')
        owner = row.get('owner')
        for key, value in [('source_ref', source), ('evidence_id', evidence_id), ('owner', owner)]:
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f'{field}: {key} must be a nonempty reference')
        refs.setdefault(evidence_id, []).append(field)
        normalized = _normalize(row, defs[field], field)
        # A p90 time statistic requires at least a minimally credible sample;
        # threshold is governance policy, NOT a statistical confidence guarantee.
        insufficient = False
        if defs[field]['method'] == 'inverse_bounded_hours':
            samples = _integer(row.get('sample_size'), field + '.sample_size')
            if samples < 0:
                raise ValueError(f'{field}: sample_size must be nonnegative')
            insufficient = samples < defs[field]['min_sample_size']
        reason = ('unverified' if row.get('verified') is not True else
                  'stale' if age > defs[field]['max_age_days'] else
                  'insufficient_sample' if insufficient else None)
        evidence[field] = {
            'usable': reason is None, 'reason': reason or 'self_attested',
            'age_days': round(age, 6), 'source_ref': source,
            'evidence_id': evidence_id, 'owner': owner,
            'normalized_when_usable': normalized if reason is None else None,
        }
        if reason is None:
            values[field] = normalized

    cov = {k: sum(f in values for f in members)/len(members) for k, members in GROUPS.items()}
    cov.update({'D_' + d: float('CS_' + d in values) for d in DOMAINS})
    r_cov = sum(f in values for f in RRAS) / len(RRAS)
    cov.update({'R_' + d: r_cov for d in DOMAINS})
    aggregate = mean(cov[k] for k in GROUPS)
    minimum = min(cov[k] for k in GROUPS)
    governing = min(cov[k] for k in ('TE', 'CM', 'SOE') +
                    tuple('D_' + d for d in DOMAINS) +
                    tuple('R_' + d for d in DOMAINS))
    gates = model_profile['coverage_gates']
    meets_gates = (aggregate >= gates['aggregate_min'] and
                   minimum >= gates['construct_min'] and
                   governing >= gates['governing_path_min'])
    unknown = [f for f in ALL if f not in values]
    lineage = {'scope_id': scope, 'as_of': as_of.isoformat(),
               'measurement_profile_id': measurement_profile['schema'],
               'model_profile_id': model_profile['profile_id'],
               'data_class': document['data_class']}
    result: dict[str, Any] = {
        'lineage': lineage, 'normalized_inputs': values, 'evidence': evidence,
        'missing_required': unknown,
        'reused_evidence_ids': {k: v for k, v in refs.items() if len(v) > 1},
        'coverage': {
            'fractions': cov, 'mean_tier2': aggregate, 'min_tier2': minimum,
            'governing_path_min': governing, 'passes_provisional_gates': meets_gates,
            'interpretation': 'self_attested_completeness_not_statistical_confidence',
        },
        'status': 'synthetic_only' if document['data_class'] == 'synthetic_demo'
                  else 'self_reported_provisional',
        'point': None, 'residual_possible_interval': None,
        'warnings': ['Calibration and raw measurement cutoffs are illustrative, not empirically validated.'],
    }
    if unknown:
        min_case, max_case = dict(values), dict(values)
        for key in unknown:
            polarity = defs[key]['polarity']
            if polarity not in ('risk', 'capacity'):
                raise ValueError(f'{key}: invalid risk/capacity polarity')
            is_adverse = polarity == 'risk'
            min_case[key] = 0.0 if is_adverse else 1.0
            max_case[key] = 1.0 if is_adverse else 0.0
        lo = _score(min_case, model_profile)['R_inst']
        hi = _score(max_case, model_profile)['R_inst']
        if lo > hi + 1e-12:
            raise AssertionError('expected monotonic residual interval inverted')
        result['residual_possible_interval'] = [lo, hi]
        result['warnings'].append('Incomplete evidence: no point CRPI; interval is feasible-value, not statistical confidence.')
        return result
    prior = document.get('prior_stock')
    if 'cold_start' in document and not isinstance(document['cold_start'], bool):
        raise ValueError('cold_start must be a boolean')
    cold = document.get('cold_start') is True
    dt = document.get('dt_days')
    if prior is not None:
        prior = _number(prior, 'prior_stock')
        if not 0.0 <= prior <= 1.0:
            raise ValueError('prior_stock must lie in [0,1]')
        dt = _number(dt, 'dt_days')
        if dt < 0:
            raise ValueError('dt_days must be nonnegative')

    if prior is None and not cold:
        result['warnings'].append('No prior stock or declared cold start: only instantaneous components calculated.')
    result['point'] = _score(values, model_profile, prior_stock=prior, dt=dt, cold_start=cold)
    if cold:
        result['warnings'].append('Cold start sets S(t0)=R_inst(t0) without reconstructing preexisting unresolved exposure.')
    if not meets_gates:
        result['warnings'].append('The provisional evidence coverage thresholds are not met.')
    result['warnings'].append('Asserted source verification is not independently checked by this program.')
    return result