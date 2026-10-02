"""Tests for bin/harness.py evaluation and routing engine."""
from pathlib import Path
import tempfile
import unittest

from bin.harness import (
    SkillEntry,
    load_all_skills,
    score_skill,
    route_query,
    check_token_budgets,
    run_benchmark,
    MAX_SKILL_LINES,
)


class HarnessTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.skills_dir = self.root / 'skills'
        self.skills_dir.mkdir(parents=True)

        self._create_mock_skill(
            name='api-design',
            pack='core',
            description='Design contract-first REST endpoints and APIs.',
            keywords=['rest', 'api', 'openapi', 'contract', 'endpoint'],
            lines=40
        )
        self._create_mock_skill(
            name='debugging',
            pack='core',
            description='Systematically diagnose bugs, stack traces, and crashes.',
            keywords=['debug', 'bug', 'crash', 'stack trace', 'trace'],
            lines=45
        )

    def _create_mock_skill(self, name: str, pack: str, description: str, keywords: list, lines: int):
        sdir = self.skills_dir / name
        sdir.mkdir(parents=True, exist_ok=True)
        kw_str = ', '.join(keywords)
        filler = '\n'.join([f"## Step {i}\nActionable instructions." for i in range(lines - 10)])
        content = f"""---
name: {name}
description: >-
  {description}
keywords: [{kw_str}]
metadata:
  pack: {pack}
---
# {name.title()}
{filler}
"""
        (sdir / 'SKILL.md').write_text(content, encoding='utf-8')

    def test_load_all_skills(self):
        skills = load_all_skills(self.skills_dir)
        self.assertEqual(2, len(skills))
        self.assertIn('api-design', skills)
        self.assertIn('debugging', skills)
        self.assertEqual('core', skills['api-design'].pack)
        self.assertTrue(len(skills['api-design'].keywords) >= 4)

    def test_score_skill_keyword_boost(self):
        skills = load_all_skills(self.skills_dir)
        score_api = score_skill('design a new rest endpoint', skills['api-design'])
        score_debug = score_skill('design a new rest endpoint', skills['debugging'])
        self.assertGreater(score_api, score_debug)

    def test_route_query(self):
        skills = load_all_skills(self.skills_dir)
        results = route_query('fix this unhandled crash and null pointer exception', skills)
        self.assertTrue(len(results) > 0)
        self.assertEqual('debugging', results[0][0])

    def test_token_budget_check_pass(self):
        skills = load_all_skills(self.skills_dir)
        ok, errors = check_token_budgets(skills)
        self.assertTrue(ok)
        self.assertEqual([], errors)

    def test_token_budget_check_fail_lines(self):
        self._create_mock_skill(
            name='bloated-skill',
            pack='core',
            description='Too many lines.',
            keywords=['bloat'],
            lines=MAX_SKILL_LINES + 20
        )
        skills = load_all_skills(self.skills_dir)
        ok, errors = check_token_budgets(skills)
        self.assertTrue(any('exceeds max lines' in err for err in errors))

    def test_harness_custom_skills_dir(self):
        from bin.harness import main
        # Test budget subcommand with custom --skills-dir
        code = main(['harness.py', 'budget', '--skills-dir', str(self.skills_dir)])
        self.assertEqual(0, code)


if __name__ == '__main__':
    unittest.main()
