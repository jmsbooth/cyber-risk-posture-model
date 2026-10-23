"""Regression checks for deterministic CRPI synthetic pressure-test methodology."""
import copy
import json
import math
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts import run_stress_tests as st
from models.crm_reference import regularized_geometric


class StressTestVerification(unittest.TestCase):
    def setUp(self):
        self.profile=json.loads(st.PROFILE_PATH.read_text(encoding='utf-8'))
        self.fields={k: .5 for k in st.FIELDS}

    def test_reference_regularized_aggregation(self):
        self.assertAlmostEqual(regularized_geometric([.55,.65],[.5,.5],.05),
                               .5980818586266033,places=13)

    def test_partial_interval_covers_truth(self):
        x=self.fields.copy()
        x.update({'TE_external':.9,'RRAS_internal':.2,'USOM_detection':.1})
        assumed, lo, hi=st.fillings(x,{'TE_external','RRAS_internal','USOM_detection'})
        y=st.score(x,self.profile)['residual']
        self.assertLessEqual(st.score(lo,self.profile)['residual'],y)
        self.assertLessEqual(y,st.score(hi,self.profile)['residual'])
        self.assertFalse(math.isnan(st.score(assumed,self.profile)['residual']))

    def test_time_order_noncommutes_but_static_semigroup_holds(self):
        result=st.cadence(self.profile)
        self.assertGreater(result['order_spread'],.1)
        self.assertLess(result['static_input_semigroup_difference'],1e-12)

    def test_seed_reproducibility_and_valid_bounds(self):
        with patch.object(st,'N',200):
            a=st.run()
            b=st.run()
        self.assertEqual(a,b)
        self.assertEqual(a['core']['boundedness_violations'],0)
        self.assertEqual(a['base_draws'],200)
        self.assertEqual(set(a['missingness']),{'mcar_10','mcar_20','risk_correlated'})

    def test_calibration_hash_is_independent_of_checkout_line_endings(self):
        # Git can check out JSON as LF on Linux and CRLF on Windows.
        # The archived numerical evidence must not depend on that setting.
        raw=st.PROFILE_PATH.read_text(encoding='utf-8')
        with tempfile.TemporaryDirectory(prefix='crpi-profile-eol-') as folder:
            lf=Path(folder)/'calibration_lf.json'
            crlf=Path(folder)/'calibration_crlf.json'
            lf.write_bytes(raw.encode('utf-8'))
            crlf.write_bytes(raw.replace('\\r\\n','\\n').replace('\\n','\\r\\n').encode('utf-8'))
            with patch.object(st,'N',100), patch.object(st,'PROFILE_PATH',lf):
                unix=st.run()
            with patch.object(st,'N',100), patch.object(st,'PROFILE_PATH',crlf):
                windows=st.run()
        self.assertEqual(unix,windows)
        self.assertEqual(unix['profile_sha256'],
                         json.loads((st.ROOT/'verification/stress_test_results.json')
                                    .read_text(encoding='utf-8'))['profile_sha256'])

    def test_archived_evidence_reproduces(self):
        artifact=st.ROOT/'verification/stress_test_results.json'
        if not artifact.exists():
            self.skipTest('archived stress output has not been generated')
        self.assertEqual(json.loads(artifact.read_text(encoding='utf-8')),st.run())


if __name__=='__main__':
    unittest.main()
