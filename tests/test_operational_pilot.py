"""Boundary and evidence-governance checks for illustrative CRPI measurement adapter."""
import copy
import json
import math
import unittest
from pathlib import Path
from unittest.mock import patch

from models.operational_pilot import ALL, evaluate
from scripts import compare_operational_baselines as baseline
from scripts.run_stress_tests import score as existing_stress_score

ROOT=Path(__file__).resolve().parents[1]


def read(path):
    return json.loads((ROOT/path).read_text(encoding='utf-8'))


class OperationalPilotTests(unittest.TestCase):
    def setUp(self):
        self.fixture=read('data/examples/operational_pilot_case.json')
        self.metric=read('config/measurement_pilot_v0.1.json')
        self.core=read('config/calibration_baseline.json')

    def evaluate(self, fixture=None, metric=None):
        return evaluate(fixture or self.fixture, metric or self.metric, self.core)

    def test_known_profile_and_all_15_primitives_complete(self):
        data=self.evaluate()
        self.assertEqual(len(ALL),15)
        self.assertEqual(set(data['normalized_inputs']),set(ALL))
        self.assertEqual(data['missing_required'],[])
        self.assertEqual(data['status'],'synthetic_only')
        self.assertTrue(data['coverage']['passes_provisional_gates'])
        self.assertAlmostEqual(data['point']['R_inst'],0.03996969804513359,places=12)
        self.assertAlmostEqual(data['point']['R_inst'],
                               existing_stress_score(data['normalized_inputs'],self.core)['residual'],
                               places=12)
        self.assertAlmostEqual(data['point']['CRPI'],0.23972394314498544,places=12)
        self.assertEqual(data['point']['history_mode'],'supplied_prior_stock')
        self.assertTrue(0.0<=data['point']['CRPI']<=1.0)

    def test_missing_observation_has_interval_but_no_crpi(self):
        data=copy.deepcopy(self.fixture)
        del data['observations']['TE_external']
        result=self.evaluate(data)
        self.assertIsNone(result['point'])
        self.assertEqual(result['missing_required'],['TE_external'])
        self.assertAlmostEqual(result['coverage']['governing_path_min'],.5)
        self.assertLess(result['residual_possible_interval'][0],
                        self.evaluate()['point']['R_inst'])
        self.assertLess(self.evaluate()['point']['R_inst'],
                        result['residual_possible_interval'][1])
        self.assertIn('not statistical confidence',' '.join(result['warnings']))

    def test_stale_verification_and_future_observations(self):
        data=copy.deepcopy(self.fixture)
        data['observations']['USOM_detection']['observed_at']='2026-01-01T00:00:00Z'
        r=self.evaluate(data)
        self.assertIsNone(r['point'])
        self.assertEqual(r['evidence']['USOM_detection']['reason'],'stale')
        data=copy.deepcopy(self.fixture)
        data['observations']['CM_integrity']['verified']=False
        r=self.evaluate(data)
        self.assertEqual(r['evidence']['CM_integrity']['reason'],'unverified')
        self.assertIsNone(r['point'])
        data=copy.deepcopy(self.fixture)
        data['observations']['RRAS_internal']['observed_at']='2026-10-24T00:00:00Z'
        with self.assertRaisesRegex(ValueError,'future-dated'):
            self.evaluate(data)

    def test_sparse_time_quantiles_cannot_be_reported_as_complete(self):
        data=copy.deepcopy(self.fixture)
        data['observations']['USOM_velocity']['sample_size']=3
        r=self.evaluate(data)
        self.assertIsNone(r['point'])
        self.assertEqual(r['evidence']['USOM_velocity']['reason'],'insufficient_sample')
        self.assertIn('USOM_velocity',r['missing_required'])

    def test_invalid_denominator_and_ordinal_cannot_be_scored(self):
        data=copy.deepcopy(self.fixture)
        data['observations']['TE_external']['denominator']=0
        with self.assertRaisesRegex(ValueError,'d > 0'):
            self.evaluate(data)
        data=copy.deepcopy(self.fixture)
        data['observations']['TE_internal']['numerator']=99
        with self.assertRaisesRegex(ValueError,'0 <= n <= d'):
            self.evaluate(data)
        data=copy.deepcopy(self.fixture)
        data['observations']['CS_integrity']['level']=4.5
        with self.assertRaisesRegex(ValueError,'integer'):
            self.evaluate(data)

    def test_missing_sources_invalid_schema_rejected(self):
        data=copy.deepcopy(self.fixture)
        data['observations']['RRAS_internal']['source_ref']=''
        with self.assertRaisesRegex(ValueError,'source_ref'):
            self.evaluate(data)
        data=copy.deepcopy(self.fixture)
        data['observations']['fake_input']={}
        with self.assertRaisesRegex(ValueError,'recognized'):
            self.evaluate(data)
        data=copy.deepcopy(self.fixture)
        data['data_class']='confirmed_calibrated'
        with self.assertRaisesRegex(ValueError,'data_class'):
            self.evaluate(data)

    def test_history_is_not_invented(self):
        data=copy.deepcopy(self.fixture)
        data['prior_stock']=None
        data.pop('cold_start',None)
        a=self.evaluate(data)
        self.assertIsNotNone(a['point']['R_inst'])
        self.assertIsNone(a['point']['CRPI'])
        self.assertEqual(a['point']['history_mode'],'not_supplied')
        data['cold_start']=True
        b=self.evaluate(data)
        self.assertAlmostEqual(b['point']['CRPI'],b['point']['R_inst'])
        self.assertEqual(b['point']['history_mode'],'declared_cold_start_t0')
        data['prior_stock']=.4
        with self.assertRaisesRegex(ValueError,'cannot be combined'):
            self.evaluate(data)

    def test_raw_unit_bound_and_denominator_sensitivity(self):
        reference=self.evaluate()['point']['R_inst']
        data=copy.deepcopy(self.fixture)
        data['observations']['TE_external']['denominator']=10
        self.assertGreater(self.evaluate(data)['point']['R_inst'],reference)
        metric=copy.deepcopy(self.metric)
        metric['fields']['USOM_velocity']['U']=24.0
        self.assertGreater(self.evaluate(metric=metric)['point']['R_inst'],reference)

    def test_output_coverage_does_not_scale_risk(self):
        base=self.evaluate()['point']['R_inst']
        data=copy.deepcopy(self.fixture)
        data['observations']['CM_coverage']['numerator']=0
        score=self.evaluate(data)
        self.assertAlmostEqual(score['normalized_inputs']['CM_coverage'],0.0)
        self.assertGreater(score['point']['R_inst'],base)
        self.assertEqual(score['coverage']['mean_tier2'],1.0)
        # An observed low monitoring score is different from absent monitoring evidence.
        bad=copy.deepcopy(data)
        bad['observations']['CM_coverage']['verified']=False
        self.assertIsNone(self.evaluate(bad)['point'])

    def test_structural_baselines_deterministic_and_nonpredictive(self):
        with patch.object(baseline,'N',60), patch.object(baseline,'PAIRS',200):
            a=baseline.run()
            b=baseline.run()
        self.assertEqual(a,b)
        self.assertTrue(a['pilot_raw_evidence_sensitivity']['missing_external_point_is_null'])
        self.assertIn('Rank disagreement is not prediction accuracy',a['claim_limits'][2])
        for obj in a['structural_baselines'].values():
            self.assertTrue(math.isfinite(obj['mean']))

    def test_archived_structural_comparisons_reproduce(self):
        self.assertEqual(baseline.run(),read('verification/measurement_pilot_structural_results.json'))


if __name__=='__main__':
    unittest.main()