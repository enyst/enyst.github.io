"""Offline regression checks for the code around the live classifier."""
import copy,json,pathlib,unittest
import run
class ContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows=json.loads(pathlib.Path(__file__).with_name('results.json').read_text())['runs']
    def test_all_recorded_responses_and_expected_ranges(self):
        self.assertTrue(all(c['passed'] for c in run.check(self.rows)))
    def test_bad_responses_are_rejected(self):
        base=next(x for x in self.rows if x['case']['group']=='triage')
        for mutation in [lambda r:r['answers'].pop('route'),lambda r:r['answers']['sufficient'].update(noul=float('nan')),lambda r:r['answers']['route'].update(choice='made_up'),lambda r:r['answers']['route'].update(probabilities={'sdk':1}),lambda r:r.update(model='unexpected')]:
            r=copy.deepcopy(base['response']);mutation(r)
            with self.assertRaises((AssertionError,KeyError)):run.validate(base['request'],r)
    def test_sufficiency_gates_even_confident_choices(self):
        case={'group':'triage'}
        self.assertEqual(run.policy(case,{'route':{'choice':'sdk','confidence':1},'sufficient':{'noul':.79}}),'human_review')
    def test_security_never_approves(self):
        for p in [0,.49,.5,1]:
            self.assertIn(run.policy({'group':'security'},{'toctou':{'noul':p},'supply_chain':{'noul':p}}),['standard_verification','priority_verification'])
    def test_closed_work_is_excluded_by_code(self):
        self.assertEqual(run.policy({'group':'interest','state':{'state':'closed'}},{}),'skip_closed')
    def test_score_cutoff_has_a_cliff(self):
        case={'group':'interest','state':{'state':'open'}}
        self.assertEqual(run.policy(case,{'interest':{'score':1.99,'confidence':.99}}),'keep_in_backlog')
        self.assertEqual(run.policy(case,{'interest':{'score':2,'confidence':.99}}),'shortlist')
if __name__=='__main__':unittest.main()
