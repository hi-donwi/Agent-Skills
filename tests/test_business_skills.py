"""Catalog-level routing regressions for business application skills.

These checks exercise the lexical router, not model execution or application security.
"""
import json
from pathlib import Path
import unittest

from bin.harness import load_all_skills, route_query


ROOT = Path(__file__).resolve().parent.parent
BUSINESS_SKILLS = {
    'saas-multitenancy', 'saas-billing', 'feature-flags', 'product-analytics',
    'saas-onboarding', 'identity-access-management', 'membership-management',
    'background-jobs', 'webhook-integrations', 'audit-logging',
    'erp-domain-design', 'erp-accounting', 'erp-inventory', 'erp-procurement',
    'erp-sales', 'workflow-approvals', 'data-import-export',
}


class BusinessSkillRoutingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.skills = load_all_skills(ROOT / 'skills')
        cls.scenarios = json.loads((ROOT / 'tests' / 'scenarios.json').read_text())['scenarios']
        cls.business = [case for case in cls.scenarios if 'target_skill' in case]

    def test_fixture_coverage_and_catalog_targets(self):
        self.assertEqual(len(self.scenarios), len({case['id'] for case in self.scenarios}))
        self.assertEqual(BUSINESS_SKILLS, {case['target_skill'] for case in self.business})
        for name in sorted(BUSINESS_SKILLS):
            with self.subTest(skill=name):
                self.assertIn(name, self.skills.keys())
                cases = [case for case in self.business if case['target_skill'] == name]
                self.assertEqual(4, len(cases))
                self.assertEqual({'direct', 'paraphrase', 'boundary', 'failure'}, {case['kind'] for case in cases})
                self.assertTrue(all(case.get('expected_decision') for case in cases if case['kind'] == 'failure'))
        for case in self.scenarios:
            with self.subTest(scenario=case['id']):
                self.assertIn(case['expected_skill'], self.skills.keys())
                self.assertEqual(case['pack'], self.skills[case['expected_skill']].pack)

    def test_all_scenarios_retrieve_expected_skill(self):
        for case in self.scenarios:
            with self.subTest(scenario=case['id']):
                results = route_query(case['query'], self.skills)
                self.assertIn(case['expected_skill'], [name for name, _ in results], results)

    def test_direct_paraphrased_and_boundary_primary_routes(self):
        for case in self.business:
            if case['kind'] == 'failure':
                continue
            with self.subTest(scenario=case['id']):
                results = route_query(case['query'], self.skills)
                self.assertTrue(results)
                self.assertEqual(case['expected_skill'], results[0][0], results)


if __name__ == '__main__':
    unittest.main()
