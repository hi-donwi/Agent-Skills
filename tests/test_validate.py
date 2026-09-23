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

    def test_bundled_template_validates(self):
        src = Path(__file__).resolve().parents[1] / 'skills/skill-creator/templates/skill-template/skill-template.md'
        dest = self.skills / 'my-skill-name'
        dest.mkdir()
        (dest / 'SKILL.md').write_text(src.read_text())
        errors = []
        validator.validate_skill(dest, errors)
        self.assertEqual([], errors)

    def test_frontmatter_comments_are_rejected(self):
        self.write(extra='# license: MIT\n')
        self.assertTrue(any('invalid frontmatter line' in error for error in self.errors()))

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

    def test_routes_to_skill_the_library_does_not_ship(self):
        self.write(body='Load `motion-design` before adding animation.')
        self.assertTrue(any('does not ship' in error for error in self.errors()))

    def test_routes_to_a_shipped_sibling_skill(self):
        (self.skills/'motion-design').mkdir()
        self.write(body='Load `motion-design` before adding animation.')
        self.assertEqual([], self.errors())

    def test_hyphenated_term_is_not_a_route_without_a_routing_verb(self):
        # Regression: a verb pattern containing 'prefers' matched inside the token.
        for body in ['- Always implement `prefers-reduced-motion` behavior.', '`prefers-reduced-motion`']:
            with self.subTest(body=body):
                self.write(body=body)
                self.assertEqual([], self.errors())

    def test_routing_pointer_inside_a_fence_is_not_a_route(self):
        self.write(body='```md\nLoad `motion-design` first.\n```')
        self.assertEqual([], self.errors())

    def test_nested_agent_instructions_are_rejected(self):
        for name in ['AGENTS.md', 'CLAUDE.md', 'GEMINI.md']:
            with self.subTest(name=name):
                target = self.skill/name
                target.write_text('# instructions')
                self.write(body=f'`{name}`')
                self.assertTrue(any('nested agent instructions' in error for error in self.errors()))
                target.unlink()

    def test_unreachable_resource_is_rejected(self):
        (self.skill/'references').mkdir()
        (self.skill/'references/orphan.md').write_text('# Orphan')
        self.write()
        self.assertTrue(any('unreachable from SKILL.md' in error for error in self.errors()))

    def test_resource_is_reachable_by_path_or_by_parent_directory(self):
        (self.skill/'references').mkdir()
        (self.skill/'references/guide.md').write_text('# Guide')
        (self.skill/'adapters').mkdir()
        (self.skill/'adapters/cursor-rule.mdc').write_text('rule')
        for body in ['`references/guide.md` and `adapters/cursor-rule.mdc`',
                     '`references/guide.md` and the `adapters/` snippets']:
            with self.subTest(body=body):
                self.write(body=body)
                self.assertEqual([], self.errors())

    def test_docs_resource_resolves_when_the_skill_ships_one(self):
        (self.skill/'docs').mkdir()
        (self.skill/'docs/real.md').write_text('# Real')
        self.write(body='`docs/real.md`')
        self.assertEqual([], self.errors())
        self.write(body='`docs/real.md` and `docs/missing.md`')
        self.assertTrue(any('dead resource' in error for error in self.errors()))

    def test_bare_docs_path_is_a_project_path_not_a_bundled_resource(self):
        self.write(body='Record the decision in `docs/adr/`.')
        self.assertEqual([], self.errors())

    def test_dead_link_in_a_reference_document_is_rejected(self):
        (self.skill/'references').mkdir()
        (self.skill/'references/guide.md').write_text('See [more](missing.md)')
        self.write(body='`references/guide.md`')
        self.assertTrue(any('dead resource' in error for error in self.errors()))

    def test_bare_resource_path_in_a_reference_resolves_against_the_skill(self):
        # A reference naming its neighbour writes `references/other.md`, the same
        # path SKILL.md would — not a path relative to its own directory.
        (self.skill/'references').mkdir()
        (self.skill/'references/other.md').write_text('# Other')
        (self.skill/'references/guide.md').write_text('See `references/other.md`')
        self.write(body='`references/guide.md`')
        self.assertEqual([], self.errors())

    def test_cursor_mdc_scheme_is_left_to_the_editor(self):
        (self.skill/'adapters').mkdir()
        (self.skill/'adapters/rule.mdc').write_text('[SKILL.md](mdc:.agents/skills/example/SKILL.md)')
        self.write(body='`adapters/rule.mdc`')
        self.assertEqual([], self.errors())

    def test_assistant_sandbox_link_is_rejected(self):
        (self.skill/'references').mkdir()
        (self.skill/'references/guide.md').write_text('[report](sandbox:/mnt/data/report.md)')
        self.write(body='`references/guide.md`')
        self.assertTrue(any('nonportable local resource' in error for error in self.errors()))

    def test_private_use_citation_markers_are_rejected(self):
        (self.skill/'references').mkdir()
        (self.skill/'references/guide.md').write_text('Codex \ue200cite\ue202turn4search1\ue201 is a coding agent.')
        self.write(body='`references/guide.md`')
        self.assertTrue(any('private-use character' in error for error in self.errors()))
        self.write(body='Arrows \u2192 and \u2264 are fine. `references/guide.md`')
        (self.skill/'references/guide.md').write_text('Clean prose.')
        self.assertEqual([], self.errors())

    def test_oversized_skill_entry_point_is_rejected(self):
        self.write(body='\n'.join(f'line {n}' for n in range(validator.MAX_SKILL_LINES)))
        self.assertTrue(any('the ceiling is' in error for error in self.errors()))

    def test_entry_point_at_the_ceiling_is_accepted(self):
        header = len(self.skill.joinpath('SKILL.md').read_text().splitlines())
        self.write(body='\n'.join(f'line {n}' for n in range(validator.MAX_SKILL_LINES - header - 1)))
        self.assertEqual([], self.errors())

    def test_malformed_url_is_diagnostic(self):
        self.write(body='[Bad](https://[invalid)')
        self.assertTrue(self.errors())

    def test_boolean_reference_count_is_rejected(self):
        self.assertTrue(self.catalog([dict(self.row(),references=False)]))

    def test_wrong_readme_target_is_rejected(self):
        self.catalog([self.row()])
        (self.root/'README.md').write_text('1 skills\n| [`example`](skills/other/SKILL.md) | Example |\n')
        errors=[]
        validator.validate_catalog(self.root, errors)
        self.assertTrue(errors)

    def catalog(self, rows, readme=None):
        (self.root/'index.json').write_text(json.dumps({'skills':rows}))
        (self.root/'README.md').write_text(readme or '1 skills\n| [`example`](skills/example/SKILL.md) | Example |\n')
        errors=[]
        validator.validate_catalog(self.root, errors)
        return errors

    def row(self):
        return {'name':'example','pack':'agent','path':'skills/example/SKILL.md','description':'Useful workflow.','references':0,'resources':0}

    def test_catalog_accepts_matching_entry(self):
        self.assertEqual([],self.catalog([self.row()]))

    def test_catalog_rejects_stale_duplicate_missing_and_wrong_path(self):
        for rows in [[],[self.row(),self.row()],[dict(self.row(),description='stale')],[dict(self.row(),path='../outside.md')],[dict(self.row(),references=4)]]:
            with self.subTest(rows=rows):
                self.assertTrue(self.catalog(rows))

    def test_readme_skill_count_must_match_and_appear_once(self):
        row = '| [`example`](skills/example/SKILL.md) | Example |\n'
        for readme in ['2 skills\n' + row, row, '1 skills and 1 skills\n' + row]:
            with self.subTest(readme=readme.splitlines()[0]):
                self.assertTrue(self.catalog([self.row()], readme=readme))

    def test_references_are_counted_apart_from_bundle_extras(self):
        (self.skill/'references').mkdir()
        (self.skill/'references/guide.md').write_text('# Guide')
        (self.skill/'adapters').mkdir()
        (self.skill/'adapters/cursor-rule.mdc').write_text('rule')
        self.assertEqual([], self.catalog([dict(self.row(), references=1, resources=1)]))
        self.assertTrue(self.catalog([dict(self.row(), references=2, resources=0)]))

    def test_catalog_malformed_json_is_diagnostic(self):
        (self.root/'index.json').write_text('{')
        errors=[]
        validator.validate_catalog(self.root, errors)
        self.assertTrue(errors)


if __name__ == '__main__':
    unittest.main()
