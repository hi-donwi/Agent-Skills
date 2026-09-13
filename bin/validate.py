#!/usr/bin/env python3
"""Validate the library's canonical metadata, local resources, and catalog.

Standard library only. This is not a general YAML or CommonMark parser: required
metadata uses plain single-line values or folded descriptions (> / >-), matching
bin/reindex. Resource checks cover inline Markdown links, link definitions, and
backtick resource paths outside fenced examples. Remote URLs and anchors are not
fetched or validated. Optional YAML metadata is outside this parser's scope.
"""
from pathlib import Path
import json
import re
import sys
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / 'skills'
PACKS = {'core', 'agent', 'web', 'java'}
RESOURCE = r'(?:references|examples|templates|scripts|assets|agents)/'
EXTENSIONS = {'.md', '.mdc', '.sh', '.js', '.mjs', '.ts', '.tsx', '.py', '.json', '.toml', '.yaml', '.yml'}


def fail(errors, skill, message):
    errors.append(f'{skill}: {message}')


def metadata(text, label, errors):
    block = re.match(r'\A---\n(.*?)\n---\n', text, re.DOTALL)
    if not block:
        fail(errors, label, 'missing opening frontmatter block')
        return {}
    lines = block.group(1).splitlines()
    values = {}
    for field in ('name', 'pack', 'description'):
        matches = [(i, re.match(rf'^{field}:[ \t]*(.*)$', line)) for i, line in enumerate(lines)]
        matches = [(i, match.group(1)) for i, match in matches if match]
        if len(matches) != 1:
            fail(errors, label, f'expected exactly one {field} field')
            continue
        i, value = matches[0]
        if value in ('>', '>-') and field == 'description':
            parts = []
            for line in lines[i + 1:]:
                if line and not line.startswith(' '):
                    break
                parts.append(line.strip())
            value = ' '.join(' '.join(parts).split())
        elif (not value or value.startswith(('"', "'", '|', '[', '{', '*', '&', '!', '#', '>'))
              or ': ' in value or ' #' in value):
            fail(errors, label, f'{field} must use canonical plain text or a folded description')
            continue
        if not value.strip():
            fail(errors, label, f'{field} is empty')
        values[field] = value
    name = values.get('name', '')
    if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', name) or len(name) > 64:
        fail(errors, label, 'name must be 1-64 lowercase alphanumerics with single hyphens')
    if values.get('pack') not in PACKS:
        fail(errors, label, 'unknown or missing pack')
    if not 1 <= len(values.get('description', '')) <= 1024:
        fail(errors, label, 'description must contain 1-1024 characters')
    return values


def without_fences(text):
    output, fence = [], None
    for line in text.splitlines():
        opening = re.match(r'^\s{0,3}(`{3,}|~{3,})', line)
        if fence:
            if re.fullmatch(r'\s{0,3}' + re.escape(fence[0]) + '{' + str(len(fence)) + r',}\s*', line):
                fence = None
        elif opening:
            fence = opening.group(1)
        else:
            output.append(line)
    return '\n'.join(output)


def resource_links(text):
    text = without_fences(text)
    links = re.findall(r'\]\(\s*(<[^>]+>|[^\s)]+)(?:\s+"[^"]*")?\s*\)', text)
    links += re.findall(r'^\s{0,3}\[[^\]]+\]:\s*(<[^>]+>|\S+)', text, re.MULTILINE)
    links += re.findall(r'`((?:[a-z0-9-]+/)?' + RESOURCE + r'[^`\s]+)`', text)
    return sorted(set(link.strip('<>') for link in links))


def validate_link(doc, link, skills_root, errors):
    label = str(doc.relative_to(skills_root))
    try:
        parsed = urlsplit(link)
    except ValueError:
        fail(errors, label, f'malformed resource URL {link!r}')
        return
    if parsed.scheme in ('https', 'http', 'mailto') or link.startswith(('#', '//')):
        return
    if parsed.scheme or Path(unquote(parsed.path)).is_absolute():
        fail(errors, label, f'nonportable local resource {link!r}')
        return
    path = unquote(parsed.path)
    if not path:
        return
    # Bare sibling resource pointers are relative to skills/, Markdown ../ links
    # are relative to the document. All targets must stay in the skill catalog.
    sibling = re.match(r'([a-z0-9-]+)/' + RESOURCE, path)
    target = skills_root / path if sibling else doc.parent / path
    try:
        resolved = target.resolve()
        resolved.relative_to(skills_root.resolve())
        if re.match(RESOURCE, path):
            resolved.relative_to(doc.parent.resolve())
        if not resolved.is_file():
            fail(errors, label, f'dead resource reference {link!r}')
    except (ValueError, RuntimeError, OSError):
        fail(errors, label, f'resource escapes catalog or cannot resolve: {link!r}')


def validate_skill(skill, errors):
    if skill.is_symlink():
        fail(errors, skill.name, 'symlink skill directory')
        return
    doc = skill / 'SKILL.md'
    if doc.is_symlink() or not doc.is_file():
        fail(errors, skill.name, 'missing or symlinked SKILL.md')
        return
    try:
        text = doc.read_text(encoding='utf-8')
    except (OSError, UnicodeError) as exc:
        fail(errors, skill.name, f'cannot read SKILL.md: {exc}')
        return
    values = metadata(text, skill.name, errors)
    if values.get('name') != skill.name:
        fail(errors, skill.name, 'frontmatter name differs from directory')
    for link in resource_links(text):
        validate_link(doc, link, skill.parent, errors)
    for path in skill.rglob('*'):
        if path.is_symlink():
            fail(errors, skill.name, f'symlink in skill tree: {path.relative_to(skill)}')
        elif path.is_file():
            if path.name == 'SKILL.md' and path != doc:
                fail(errors, skill.name, 'nested SKILL.md leaks into discovery')
            if path.suffix not in EXTENSIONS:
                fail(errors, skill.name, f'unexpected file type {path.name!r}')


def validate_catalog(root, errors):
    skills_root = root / 'skills'
    try:
        index = json.loads((root / 'index.json').read_text())
        rows = index['skills']
        if not isinstance(rows, list) or any(not isinstance(row, dict) for row in rows):
            raise ValueError('skills must be an array of objects')
        names = [row.get('name') for row in rows]
        if any(not isinstance(name, str) for name in names):
            raise ValueError('every entry needs a string name')
        if any(type(row.get('references')) is not int or row['references'] < 0 for row in rows):
            raise ValueError('references must be a nonnegative integer')
    except (OSError, ValueError, KeyError, TypeError) as exc:
        fail(errors, 'catalog', f'invalid index.json: {exc}')
        return
    directories = sorted(p for p in skills_root.iterdir() if p.is_dir() and not p.name.startswith('.'))
    expected = {p.name for p in directories}
    if len(names) != len(set(names)) or set(names) != expected:
        fail(errors, 'catalog', 'index membership is missing, extra, or duplicated')
    by_name = {row['name']: row for row in rows}
    for skill in directories:
        if skill.is_symlink() or not (skill/'SKILL.md').is_file() or (skill/'SKILL.md').is_symlink():
            continue
        try:
            values = metadata((skill/'SKILL.md').read_text(), skill.name, [])
        except (OSError, UnicodeError):
            continue  # validate_skill reports the read failure.
        expected_row = dict(values, path=f'skills/{skill.name}/SKILL.md',
                            references=sum(p.is_file() and p.name != 'SKILL.md' for p in skill.rglob('*')))
        row = by_name.get(skill.name, {})
        if any(row.get(key) != value for key, value in expected_row.items()):
            fail(errors, skill.name, 'stale index entry; run ./bin/reindex')
    try:
        readme = (root/'README.md').read_text()
        listed = re.findall(r'^\| \[`([^`]+)`\]\(skills/[^)]+\)', readme, re.MULTILINE)
        if len(listed) != len(set(listed)) or set(listed) != expected:
            fail(errors, 'catalog', 'README skill membership is missing, extra, or duplicated')
        for name, target in re.findall(r'^\| \[`([^`]+)`\]\((skills/[^)]+)\)', readme, re.MULTILINE):
            if target != f'skills/{name}/SKILL.md':
                fail(errors, 'catalog', f'wrong README target for {name}')
    except (OSError, UnicodeError) as exc:
        fail(errors, 'catalog', f'cannot read README: {exc}')


def main():
    if not SKILLS.is_dir():
        print(f'skills/ not found at {SKILLS}', file=sys.stderr)
        return 2
    errors = []
    dirs = sorted(p for p in SKILLS.iterdir() if p.is_dir() and not p.name.startswith('.'))
    for skill in dirs:
        validate_skill(skill, errors)
    if not dirs:
        errors.append('catalog: no skills discovered')
    validate_catalog(ROOT, errors)
    for error in errors:
        print(f'::error::{error}')
    print(f'validated {len(dirs)} skills, {len(errors)} problem(s)')
    return 1 if errors else 0


if __name__ == '__main__':
    sys.exit(main())
