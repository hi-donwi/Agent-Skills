#!/usr/bin/env python3
"""Validates the skill catalog: frontmatter, references, and discovery.

Zero dependencies (Python 3 standard library only). Checks what CI cannot
grep for and what reindex does not look at:

- every skills/*/SKILL.md has name, pack, and description frontmatter,
  with the directory and the frontmatter name agreeing
- every `references/...` / `examples/...` path quoted in a SKILL.md resolves
  inside that skill directory (cross-skill pointers must name the skill
  explicitly, e.g. `webapp-testing/references/devtools-mcp.md`)
- template directories (skills/*/templates/) carry no SKILL.md, so nested
  examples can never be discovered as skills
- every skill directory contains only expected file types
"""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"

# Resources must live inside the skill's own directory under these roots.
LOCAL_RESOURCE_PREFIXES = ("references/", "examples/")


def fail(errors, skill, message):
    errors.append(f"{skill}: {message}")


def validate_skill(skill: Path, errors):
    doc = skill / "SKILL.md"
    if not doc.is_file():
        fail(errors, skill.name, "missing SKILL.md")
        return
    text = doc.read_text(encoding="utf-8")

    frontmatter = re.match(r"\A---\n(.*?)\n---\n", text, re.DOTALL)
    if not frontmatter:
        fail(errors, skill.name, "SKILL.md does not start with a frontmatter block")
        frontmatter = None
    fm_text = frontmatter.group(1) if frontmatter else ""
    for field in ("name", "pack", "description"):
        if not re.search(rf"^{field}:\s*\S", fm_text, re.MULTILINE):
            fail(errors, skill.name, f"frontmatter is missing '{field}:'")
    name = re.search(r"^name:\s*(\S+)", fm_text, re.MULTILINE)
    if name and name.group(1) != skill.name:
        fail(errors, skill.name, f"frontmatter name '{name.group(1)}' != directory name")

    for rel in sorted(set(re.findall(r"`((?:references|examples)/[^`\s]+)`", text))):
        target = skill / rel
        if not target.is_file():
            fail(errors, skill.name, f"dead resource reference '{rel}'")
        try:
            target.resolve().relative_to(skill.resolve())
        except ValueError:
            fail(errors, skill.name, f"reference '{rel}' escapes the skill directory")

    for other in sorted(set(re.findall(r"`([a-z0-9-]+/(?:references|examples)/[^`\s]+)`", text))):
        if not (SKILLS / other).is_file():
            fail(errors, skill.name, f"dead cross-skill reference '{other}'")

    if (skill / "templates").is_dir():
        if any((skill / "templates").rglob("SKILL.md")):
            fail(errors, skill.name, "template directory contains a SKILL.md (leaks into discovery)")

    for path in skill.rglob("*"):
        if path.is_file() and path.suffix not in {".md", ".mdc", ".sh", ".js", ".mjs", ".ts", ".tsx", ".py", ".json", ".toml", ".yaml", ".yml"}:
            fail(errors, skill.name, f"unexpected file type '{path.name}'")
        if path.is_symlink():
            fail(errors, skill.name, f"symlink in skill tree: {path.relative_to(skill)}")


def main() -> int:
    if not SKILLS.is_dir():
        print(f"skills/ not found at {SKILLS}", file=sys.stderr)
        return 2
    errors = []
    dirs = sorted(p for p in SKILLS.iterdir() if p.is_dir() and not p.name.startswith("."))
    for skill in dirs:
        validate_skill(skill, errors)
    if not dirs:
        errors.append("catalog: no skills discovered")
    for error in errors:
        print(f"::error::{error}")
    print(f"validated {len(dirs)} skills, {len(errors)} problem(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
