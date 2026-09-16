"""Regression checks using disposable skill catalogs, no network or dependencies."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('validator', Path(__file__).resolve().parents[1] / 'bin/validate.py')
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


class ValidationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.skills = self.root / 'skills'
        self.skill = self.skills / 'example'
        self.skill.mkdir(parents=True)
        self.patch = patch.object(validator, 'SKILLS', self.skills)
        self.patch.start()
        self.addCleanup(self.patch.stop)
        self.write()

    def write(self, name='example', pack='agent', description='Useful workflow.', body='', extra='', meta_extra=''):
        (self.skill / 'SKILL.md').write_text(
            f'---\nname: {name}\ndescription: {description}\n{extra}'
            f'metadata:\n  pack: {pack}\n{meta_extra}---\n# Example\n{body}\n'
        )

    def errors(self):
        errors = []
        validator.validate_skill(self.skill, errors)
        return errors

    def test_valid_skill(self):
        self.assertEqual([], self.errors())

    def test_invalid_names(self):
        for name in ['Upper', '-example', 'example-', 'two--words', 'a' * 65]:
            with self.subTest(name=name):
                self.skill = self.skills / name
                self.skill.mkdir()
                self.write(name=name)
                self.assertTrue(self.errors())

    def test_unknown_pack(self):
        self.write(pack='missing-pack')
        self.assertTrue(self.errors())

    def test_top_level_pack_is_rejected(self):
        self.write(extra='pack: core\n')
        self.assertTrue(any('unexpected field' in error for error in self.errors()))

    def test_unknown_top_level_field_is_rejected(self):
        self.write(extra='keywords: example\n')
        self.assertTrue(any('unexpected field' in error for error in self.errors()))

    def test_optional_spec_fields_are_allowed(self):
        self.write(extra='license: MIT\ncompatibility: Requires git\nallowed-tools: Read\n')
        self.assertEqual([], self.errors())

    def test_metadata_extra_string_keys_are_allowed(self):
        self.write(meta_extra='  version: 1.0\n')
        self.assertEqual([], self.errors())

    def test_oversized_compatibility_is_rejected(self):
        self.write(extra=f'compatibility: {"x" * 501}\n')
        self.assertTrue(self.errors())

    def test_flow_style_metadata_is_rejected(self):
        (self.skill / 'SKILL.md').write_text(
            '---\nname: example\ndescription: Useful workflow.\nmetadata: {pack: agent}\n---\n# Example\n'
        )
        self.assertTrue(self.errors())

    def test_missing_metadata_pack_is_rejected(self):
        (self.skill / 'SKILL.md').write_text(
            '---\nname: example\ndescription: Useful workflow.\n---\n# Example\n'
        )
        self.assertTrue(any('metadata.pack' in error for error in self.errors()))

    def test_empty_and_oversized_descriptions(self):
        for value in ['>-', "''", '""', 'x' * 1025]:
            with self.subTest(value=value[:30]):
                self.write(description=value)
                self.assertTrue(self.errors())

    def test_invalid_plain_yaml_value(self):
        for description in ['workflow: invalid mapping', 'workflow # silently truncated']:
            with self.subTest(description=description):
                self.write(description=description)
                self.assertTrue(self.errors())

    def test_folded_description(self):
        self.write(description='>-\n  Useful workflow\n  for testing.')
        self.assertEqual([], self.errors())

    def test_duplicate_required_field(self):
        self.write(extra='name: other\n')
        self.assertTrue(self.errors())

    def test_missing_markdown_resources(self):
        for body in ['[Guide](references/missing.md)', '[Template](templates/missing.md)', '`scripts/missing.py`', '[Guide][guide]\n\n[guide]: references/missing.md']:
            with self.subTest(body=body):
                self.write(body=body)
                self.assertTrue(self.errors())

    def test_existing_resources_and_external_links(self):
        (self.skill/'references').mkdir()
        (self.skill/'references/guide.md').write_text('# Guide')
        self.write(body='[Guide](references/guide.md#guide) [External](https://example.invalid/a) [Here](#example)')
        self.assertEqual([], self.errors())

    def test_fenced_examples_are_not_live_links(self):
        self.write(body='```md\n[example](references/not-real.md)\n```')
        self.assertEqual([], self.errors())

    def test_escape_and_symlinks(self):
        outside=self.root/'private.md'; outside.write_text('fixture')
        self.write(body='[Outside](../../private.md)')
        self.assertTrue(self.errors())
        self.write()
        (self.skill/'leak.md').symlink_to(outside)
        self.assertTrue(self.errors())

    def test_nested_discoverable_entrypoint(self):
        (self.skill/'assets').mkdir()
        (self.skill/'assets/SKILL.md').write_text('# accidental skill')
        self.assertTrue(self.errors())

    def test_sibling_resource_escape(self):
        sibling=self.skills/'sibling'; sibling.mkdir()
        (sibling/'references').mkdir()
        (sibling/'references/leak.md').symlink_to(self.root/'outside.md')
        (self.root/'outside.md').write_text('fixture')
        self.write(body='`sibling/references/leak.md`')
        self.assertTrue(self.errors())

    def test_local_resource_cannot_traverse_into_sibling(self):
        sibling=self.skills/'sibling'; sibling.mkdir()
        (sibling/'guide.md').write_text('# Guide')
        self.write(body='`references/../../sibling/guide.md`')
        self.assertTrue(self.errors())

    def test_malformed_url_is_diagnostic(self):
        self.write(body='[Bad](https://[invalid)')
        self.assertTrue(self.errors())

    def test_boolean_reference_count_is_rejected(self):
        self.assertTrue(self.catalog([dict(self.row(),references=False)]))

    def test_wrong_readme_target_is_rejected(self):
        self.catalog([self.row()])
        (self.root/'README.md').write_text('| [`example`](skills/other/SKILL.md) | Example |\n')
        errors=[]
        validator.validate_catalog(self.root, errors)
        self.assertTrue(errors)

    def catalog(self, rows):
        (self.root/'index.json').write_text(json.dumps({'skills':rows}))
        (self.root/'README.md').write_text('| [`example`](skills/example/SKILL.md) | Example |\n')
        errors=[]
        validator.validate_catalog(self.root, errors)
        return errors

    def row(self):
        return {'name':'example','pack':'agent','path':'skills/example/SKILL.md','description':'Useful workflow.','references':0}

    def test_catalog_accepts_matching_entry(self):
        self.assertEqual([],self.catalog([self.row()]))

    def test_catalog_rejects_stale_duplicate_missing_and_wrong_path(self):
        for rows in [[],[self.row(),self.row()],[dict(self.row(),description='stale')],[dict(self.row(),path='../outside.md')],[dict(self.row(),references=4)]]:
            with self.subTest(rows=rows):
                self.assertTrue(self.catalog(rows))

    def test_catalog_malformed_json_is_diagnostic(self):
        (self.root/'index.json').write_text('{')
        errors=[]
        validator.validate_catalog(self.root, errors)
        self.assertTrue(errors)


if __name__ == '__main__':
    unittest.main()
