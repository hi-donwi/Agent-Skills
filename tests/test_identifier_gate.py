"""Regression checks for bin/identifier-gate.sh, using disposable trees only.

The gate exists to keep private names out of published files, so the tests use
invented names and assert both directions: a private name fails the build, and a
name on the public list does not.
"""
import os
from pathlib import Path
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parent.parent
GATE = ROOT / 'bin' / 'identifier-gate.sh'
PRIVATE = 'zzprivateclient'
PUBLIC = 'zzpublicproject'


class IdentifierGateTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.skills = self.root / 'skills'
        self.skills.mkdir()
        self.allowlist = self.root / 'public-identifiers'
        self.allowlist.write_text(f'# comment\n\n{PUBLIC}\n')

    def run_gate(self, pattern=f'{PRIVATE}|{PUBLIC}'):
        env = dict(os.environ, PRIVATE_IDENTIFIERS=pattern, IDENTIFIER_ALLOWLIST=str(self.allowlist))
        return subprocess.run(
            ['bash', str(GATE), str(self.skills)],
            capture_output=True, text=True, env=env, cwd=str(ROOT), check=False,
        )

    def write_skill(self, name, body):
        (self.skills / name).mkdir()
        (self.skills / name / 'SKILL.md').write_text(f'---\nname: {name}\n---\n{body}\n')

    def test_private_name_fails_and_names_only_the_file(self):
        self.write_skill('leaky', f'Worked through this with {PRIVATE} last quarter.')
        result = self.run_gate()
        self.assertEqual(1, result.returncode, result.stdout)
        self.assertIn(f'a personal or client name reached a published file: {self.skills / "leaky" / "SKILL.md"}', result.stdout)
        self.assertNotIn(PRIVATE, result.stdout)

    def test_public_name_passes(self):
        self.write_skill('clean', f'The {PUBLIC} package ships a uidl document.')
        result = self.run_gate()
        self.assertEqual(0, result.returncode, result.stdout)

    def test_case_insensitive_against_the_public_list(self):
        self.allowlist.write_text(f'{PUBLIC.upper()}\n')
        self.write_skill('clean', f'The {PUBLIC} package ships a uidl document.')
        self.assertEqual(0, self.run_gate().returncode)

    def test_one_private_file_among_public_names_fails(self):
        self.write_skill('clean', f'The {PUBLIC} package is fine.')
        self.write_skill('leaky', f'Owned by {PRIVATE}.')
        result = self.run_gate()
        self.assertEqual(1, result.returncode)
        self.assertIn('/leaky/SKILL.md', result.stdout)
        self.assertNotIn('/clean/SKILL.md', result.stdout)

    def test_home_directory_path_fails(self):
        self.write_skill('paths', 'Open /Users/example/notes before editing.')
        result = self.run_gate()
        self.assertEqual(1, result.returncode, result.stdout)
        self.assertIn('a home-directory path reached a published file', result.stdout)
        self.assertNotIn('/Users/example', result.stdout)

    def test_api_path_is_not_a_home_directory(self):
        self.write_skill('paths', 'The endpoint is /api/users/profile.')
        self.assertEqual(0, self.run_gate().returncode)

    def test_unset_pattern_warns_and_passes(self):
        self.write_skill('leaky', f'Owned by {PRIVATE}.')
        result = self.run_gate(pattern='')
        self.assertEqual(0, result.returncode, result.stdout)
        self.assertIn('PRIVATE_IDENTIFIERS is unset', result.stdout)

    def test_missing_public_list_fails_closed(self):
        self.write_skill('leaky', f'Owned by {PRIVATE}.')
        self.allowlist.unlink()
        result = self.run_gate()
        self.assertEqual(1, result.returncode, result.stdout)
        self.assertIn('public identifier list is unreadable', result.stdout)

    def test_published_catalog_passes_with_the_repository_public_list(self):
        pattern = 'donwi|hi-donwi|uidl-runtime'
        env = dict(os.environ, PRIVATE_IDENTIFIERS=pattern)
        result = subprocess.run(
            ['bash', str(GATE), str(ROOT / 'skills')],
            capture_output=True, text=True, env=env, cwd=str(ROOT), check=False,
        )
        self.assertEqual(0, result.returncode, result.stdout)


if __name__ == '__main__':
    unittest.main()