#!/usr/bin/env python3
"""Validate the library's canonical metadata, local resources, and catalog.

Standard library only. This is not a general YAML or CommonMark parser: required
name/description use plain single-line values or a folded description (> / >-),
and pack lives under a block `metadata` map, matching bin/reindex. Resource
checks cover inline Markdown links, link definitions, and backtick resource
paths outside fenced examples. Remote URLs and anchors are not fetched or
validated. Flow-style YAML and nested metadata values are rejected.

Beyond resources, three checks guard what a reader can actually follow:
cross-skill pointers must name a skill the library ships, no file may pose as
agent instructions for the surrounding project, and every bundled file must be
reachable from its SKILL.md.
"""
from pathlib import Path
import json
import re
import sys
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / 'skills'
PACKS = {'core', 'agent', 'web', 'java'}
ALLOWED_FIELDS = {'name', 'description', 'license', 'compatibility', 'allowed-tools', 'metadata'}
RESOURCE = r'(?:references|examples|templates|scripts|assets|agents|docs)/'
# Unlike references/ or scripts/, `docs/` names a directory the reader's own repo
# usually has, so `docs/adr/` in prose is a project path. Only resolve it against
# a skill that ships one.
SKILL_OWNED_ONLY = ('docs/',)
EXTENSIONS = {'.md', '.mdc', '.sh', '.js', '.mjs', '.ts', '.tsx', '.py', '.json', '.toml', '.yaml', '.yml'}
MAX_COMPATIBILITY = 500
# Files an agent walking the directory tree reads as instructions for the project
# it is working in, not as this skill's reference material.
AGENT_INSTRUCTIONS = {'AGENTS.md', 'CLAUDE.md', 'GEMINI.md', '.cursorrules', '.windsurfrules'}
ROUTING_VERB = re.compile(r'\b(?:use|uses|using|load|loads|loading|see|prefer|'
                          r'switch to|chain to|route|routes|delegate|escalate)\b', re.IGNORECASE)
# 'prefers' is excluded on purpose: it would match inside `prefers-reduced-motion`.
SKILL_TOKEN = re.compile(r'`([a-z0-9]+(?:-[a-z0-9]+)+)`')


def fail(errors, skill, message):
    errors.append(f'{skill}: {message}')


def invalid_scalar(value):
    return (not value or value.startswith(('"', "'", '|', '[', '{', '*', '&', '!', '#', '>'))
            or ': ' in value or ' #' in value)


def parse_frontmatter(text, label, errors):
    """Parse required Agent Skills fields plus this library's metadata.pack."""
    block = re.match(r'\A---\n(.*?)\n---\n', text, re.DOTALL)
    if not block:
        fail(errors, label, 'missing opening frontmatter block')
        return {}
    lines = block.group(1).splitlines()
    values = {}
    metadata = {}
    seen = set()
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        match = re.match(r'^([A-Za-z0-9_-]+):[ \t]*(.*)$', line)
        if not match:
            fail(errors, label, f'invalid frontmatter line {line!r}')
            i += 1
            continue
        field, value = match.group(1), match.group(2)
        if field not in ALLOWED_FIELDS:
            fail(errors, label, f'unexpected field {field!r}; only {sorted(ALLOWED_FIELDS)} are allowed')
            i += 1
            continue
        if field in seen:
            fail(errors, label, f'expected exactly one {field} field')
            i += 1
            continue
        seen.add(field)
        if field == 'metadata':
            if value.strip():
                fail(errors, label, 'metadata must be a block mapping')
                i += 1
                continue
            i += 1
            while i < len(lines):
                nested_line = lines[i]
                if not nested_line.strip():
                    i += 1
                    continue
                nested = re.match(r'^([ \t]+)([A-Za-z0-9_-]+):[ \t]*(.*)$', nested_line)
                if not nested:
                    break
                key, nested_value = nested.group(2), nested.group(3)
                if key in metadata:
                    fail(errors, label, f'expected exactly one metadata.{key} field')
                elif nested_value in ('>', '>-') or invalid_scalar(nested_value):
                    fail(errors, label, f'metadata.{key} must use canonical plain text')
                elif not nested_value.strip():
                    fail(errors, label, f'metadata.{key} is empty')
                else:
                    metadata[key] = nested_value.strip()
                i += 1
            continue
        if value in ('>', '>-') and field == 'description':
            parts = []
            i += 1
            while i < len(lines):
                cont = lines[i]
                if cont and not cont.startswith((' ', '\t')):
                    break
                parts.append(cont.strip())
                i += 1
            value = ' '.join(' '.join(parts).split())
            if not value.strip():
                fail(errors, label, 'description is empty')
            else:
                values[field] = value
            continue
        if invalid_scalar(value):
            fail(errors, label, f'{field} must use canonical plain text or a folded description')
            i += 1
            continue
        stripped = value.strip()
        if not stripped:
            fail(errors, label, f'{field} is empty')
            i += 1
            continue
        values[field] = stripped
        i += 1
    for field in ('name', 'description'):
        if field not in seen:
            fail(errors, label, f'expected exactly one {field} field')
    name = values.get('name', '')
    if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', name) or len(name) > 64:
        fail(errors, label, 'name must be 1-64 lowercase alphanumerics with single hyphens')
    if not 1 <= len(values.get('description', '')) <= 1024:
        fail(errors, label, 'description must contain 1-1024 characters')
    if 'compatibility' in values and not 1 <= len(values['compatibility']) <= MAX_COMPATIBILITY:
        fail(errors, label, 'compatibility must contain 1-500 characters')
    pack = metadata.get('pack', '')
    if pack not in PACKS:
        fail(errors, label, 'unknown or missing metadata.pack')
    values['pack'] = pack
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


def skill_pointers(text):
    """Backticked skill-shaped tokens on lines that send the agent somewhere else.

    Deliberately narrow, because a hyphenated token is not by itself a claim that
    a skill exists: `prefers-reduced-motion` in a rule is not a route, while
    "Load `motion-design`" is. Only a routing verb on the same line promotes the
    token to a pointer. A term that reads like a route but is not one should be
    rephrased rather than added to an allowlist.
    """
    found = set()
    for line in without_fences(text).splitlines():
        if ROUTING_VERB.search(line):
            found.update(SKILL_TOKEN.findall(line))
    return found


def unreachable_resources(skill, text):
    """Bundled files that SKILL.md never names, by path or by parent directory.

    Reachability is a weaker claim than a live link: it is satisfied anywhere in
    the document, fenced examples included, because the point is only that a
    reader is told the file is there. Liveness is validate_link's job.
    """
    for path in sorted(skill.rglob('*')):
        if not path.is_file() or path.name == 'SKILL.md':
            continue
        relative = path.relative_to(skill).as_posix()
        parent = path.parent.relative_to(skill).as_posix()
        if relative in text or (parent != '.' and f'{parent}/' in text):
            continue
        yield relative


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
    if path.startswith(SKILL_OWNED_ONLY) and not (doc.parent / path.split('/')[0]).is_dir():
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
    values = parse_frontmatter(text, skill.name, errors)
    if values.get('name') != skill.name:
        fail(errors, skill.name, 'frontmatter name differs from directory')
    for link in resource_links(text):
        validate_link(doc, link, skill.parent, errors)
    shipped = {p.name for p in skill.parent.iterdir() if p.is_dir() and not p.name.startswith('.')}
    for pointer in sorted(skill_pointers(text) - shipped):
        fail(errors, skill.name, f'routes to skill {pointer!r}, which this library does not ship')
    for orphan in unreachable_resources(skill, text):
        fail(errors, skill.name, f'{orphan!r} is unreachable from SKILL.md')
    for path in skill.rglob('*'):
        if path.is_symlink():
            fail(errors, skill.name, f'symlink in skill tree: {path.relative_to(skill)}')
        elif path.is_file():
            if path.name == 'SKILL.md' and path != doc:
                fail(errors, skill.name, 'nested SKILL.md leaks into discovery')
            if path.name in AGENT_INSTRUCTIONS:
                fail(errors, skill.name,
                     f'nested agent instructions {path.relative_to(skill).as_posix()!r} leak into discovery')
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
        for field in ('references', 'resources'):
            if any(type(row.get(field)) is not int or row[field] < 0 for row in rows):
                raise ValueError(f'{field} must be a nonnegative integer')
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
            values = parse_frontmatter((skill/'SKILL.md').read_text(), skill.name, [])
        except (OSError, UnicodeError):
            continue  # validate_skill reports the read failure.
        expected_row = {
            'name': values.get('name'),
            'pack': values.get('pack'),
            'path': f'skills/{skill.name}/SKILL.md',
            'description': values.get('description'),
            'references': sum(p.is_file() and p.relative_to(skill).parts[0] == 'references'
                              for p in skill.rglob('*')),
            'resources': sum(p.is_file() and p.name != 'SKILL.md'
                             and p.relative_to(skill).parts[0] != 'references'
                             for p in skill.rglob('*')),
        }
        row = by_name.get(skill.name, {})
        if any(row.get(key) != value for key, value in expected_row.items()):
            fail(errors, skill.name, 'stale index entry; run ./bin/reindex')
    try:
        readme = (root/'README.md').read_text()
        declared = re.findall(r'\b(\d+) skills\b', readme)
        if len(declared) != 1:
            fail(errors, 'catalog', 'README must declare the skill count exactly once as "<n> skills"')
        elif int(declared[0]) != len(expected):
            fail(errors, 'catalog', f'README says {declared[0]} skills; the catalog has {len(expected)}')
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
