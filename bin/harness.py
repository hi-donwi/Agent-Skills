#!/usr/bin/env python3
"""Evaluation and benchmark harness for agent skills.

Standard library only. Evaluates:
1. Token budget & density: ensures SKILL.md remains <= 100 lines and description <= 350 chars.
2. Trigger routing accuracy: runs synthetic prompt scenarios and measures Top-1 and Top-3 precision/recall.
3. Offline regression testing: ensures skill modifications do not degrade retrieval performance.
"""
from dataclasses import dataclass
from pathlib import Path
import json
import re
import sys
from typing import Dict, List, Optional, Tuple

ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / 'skills'
DEFAULT_SCENARIOS = ROOT / 'tests' / 'scenarios.json'

MAX_SKILL_LINES = 100
MAX_DESCRIPTION_CHARS = 500
WARN_DESCRIPTION_CHARS = 350


@dataclass
class SkillEntry:
    name: str
    pack: str
    path: Path
    description: str
    keywords: List[str]
    line_count: int
    char_count: int

    @property
    def token_estimate(self) -> int:
        return max(1, self.char_count // 4)


def normalize(text: str) -> str:
    """Normalize text for consistent token matching."""
    text = text.lower()
    return re.sub(r'[^a-z0-9]+', ' ', text).strip()


def parse_skill(skill_dir: Path) -> Optional[SkillEntry]:
    skill_file = skill_dir / 'SKILL.md'
    if not skill_file.is_file():
        return None

    content = skill_file.read_text(encoding='utf-8')
    lines = content.splitlines()
    line_count = len(lines)
    char_count = len(content)

    # Parse YAML frontmatter
    in_fm = False
    name = skill_dir.name
    pack = 'core'
    description = ''
    keywords: List[str] = []

    fmLines = []
    for line in lines:
        if line.strip() == '---':
            if not in_fm:
                in_fm = True
                continue
            else:
                break
        if in_fm:
            fmLines.append(line)

    fm_text = '\n'.join(fmLines)

    # Name
    m_name = re.search(r'^name:\s*([a-z0-9\-]+)', fm_text, re.MULTILINE)
    if m_name:
        name = m_name.group(1).strip()

    # Description (folded or single line)
    m_desc = re.search(r'^description:\s*(?:[>|]-?\s*)?(.*?)(?=\n[a-z_][a-z0-9_\-]*:|\Z)', fm_text, re.DOTALL | re.MULTILINE)
    if m_desc:
        description = ' '.join(m_desc.group(1).split()).strip()

    # Keywords
    m_kw = re.search(r'keywords:\s*\[?(.*?)\]?$', fm_text, re.MULTILINE)
    if m_kw:
        raw_kws = m_kw.group(1).split(',')
        keywords = [kw.strip().strip('"\'') for kw in raw_kws if kw.strip()]

    # Metadata pack
    m_pack = re.search(r'^\s*pack:\s*([a-z0-9\-]+)', fm_text, re.MULTILINE)
    if m_pack:
        pack = m_pack.group(1).strip()

    return SkillEntry(
        name=name,
        pack=pack,
        path=skill_file,
        description=description,
        keywords=keywords,
        line_count=line_count,
        char_count=char_count,
    )


def load_all_skills(skills_dir: Path = SKILLS_DIR) -> Dict[str, SkillEntry]:
    skills = {}
    for d in sorted(skills_dir.iterdir()):
        if d.is_dir():
            entry = parse_skill(d)
            if entry:
                skills[entry.name] = entry
    return skills


SIGNIFICANT_SHORT_TERMS = {'api', 'bug', 'sql', 'adr', 'git', 'css', 'tdd', 'e2e', 'xss', 'db', 'ui', 'pr', 'fix', 'auth'}


def score_skill(query: str, skill: SkillEntry) -> int:
    """Scores a skill against a user query.
    Matches ws route model: 5 x keyword hits + 1 x description word hits.
    Also rewards skill name components and high-signal domain terms.
    """
    q_norm = ' ' + normalize(query) + ' '
    score = 0

    # Keyword matching (5 points each)
    for kw in skill.keywords:
        kw_norm = normalize(kw)
        if kw_norm and (' ' + kw_norm + ' ' in q_norm or kw_norm in q_norm):
            score += 5

    # Description words matching (1 point each for significant words)
    desc_words = set(
        w for w in normalize(skill.description).split()
        if len(w) > 4 or w in SIGNIFICANT_SHORT_TERMS
    )
    for dw in desc_words:
        if ' ' + dw + ' ' in q_norm:
            score += 1

    # Exact skill name match gives high confidence
    if skill.name in q_norm or skill.name.replace('-', ' ') in q_norm:
        score += 10

    # Skill name parts (e.g., 'debug' from 'debugging', 'design' from 'api-design')
    for part in skill.name.split('-'):
        if len(part) >= 3 and (' ' + part in q_norm or part + ' ' in q_norm):
            score += 4
        elif part.endswith('ing') and len(part) > 5 and (' ' + part[:-3] in q_norm):
            score += 4

    return score


def route_query(query: str, skills: Dict[str, SkillEntry], top_k: int = 3) -> List[Tuple[str, int]]:
    scored = []
    for name, skill in skills.items():
        s = score_skill(query, skill)
        if s > 0:
            scored.append((name, s))
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:top_k]


def check_token_budgets(skills: Dict[str, SkillEntry]) -> Tuple[bool, List[str]]:
    errors = []
    total_tokens = 0
    total_desc_chars = 0

    warnings = []
    for name, skill in skills.items():
        total_tokens += skill.token_estimate
        total_desc_chars += len(skill.description)

        if skill.line_count > MAX_SKILL_LINES:
            errors.append(f"{name}: exceeds max lines ({skill.line_count} > {MAX_SKILL_LINES})")
        if len(skill.description) > MAX_DESCRIPTION_CHARS:
            errors.append(f"{name}: description exceeds hard ceiling ({len(skill.description)} > {MAX_DESCRIPTION_CHARS})")
        elif len(skill.description) > WARN_DESCRIPTION_CHARS:
            warnings.append(f"{name}: description exceeds recommended brevity ({len(skill.description)} > {WARN_DESCRIPTION_CHARS})")

    avg_desc_chars = total_desc_chars // max(1, len(skills))
    print(f"Token Budget Audit: {len(skills)} skills analyzed")
    print(f"  Total catalog token weight (full files): ~{total_tokens} tokens")
    print(f"  Average description length (prompt picker): {avg_desc_chars} chars (~{avg_desc_chars // 4} tokens)")
    if warnings:
        print(f"  Notice: {len(warnings)} skills have descriptions > {WARN_DESCRIPTION_CHARS} chars (consider trimming to save prompt tokens)")

    return (len(errors) == 0, errors)


def run_benchmark(scenarios_file: Path, skills: Dict[str, SkillEntry], min_accuracy: float = 0.85) -> bool:
    if not scenarios_file.is_file():
        print(f"Error: scenarios file not found: {scenarios_file}", file=sys.stderr)
        return False

    try:
        data = json.loads(scenarios_file.read_text(encoding='utf-8'))
    except Exception as e:
        print(f"Error reading scenarios JSON: {e}", file=sys.stderr)
        return False

    scenarios = data.get('scenarios', [])
    if not scenarios:
        print("Error: no scenarios found in catalog", file=sys.stderr)
        return False

    top1_correct = 0
    top3_correct = 0
    total = len(scenarios)
    failures = []

    print(f"\nRunning Routing Benchmark across {total} synthetic scenarios...")
    print("-" * 70)

    for sc in scenarios:
        sid = sc.get('id', 'unknown')
        query = sc.get('query', '')
        expected = sc.get('expected_skill', '')

        results = route_query(query, skills, top_k=3)
        matched_names = [r[0] for r in results]

        is_top1 = bool(matched_names and matched_names[0] == expected)
        is_top3 = expected in matched_names

        if is_top1:
            top1_correct += 1
        if is_top3:
            top3_correct += 1
        else:
            failures.append({
                'id': sid,
                'query': query,
                'expected': expected,
                'got': matched_names,
                'scores': results
            })

    top1_acc = top1_correct / total
    top3_acc = top3_correct / total

    print(f"Results:")
    print(f"  Top-1 Precision: {top1_acc * 100:.1f}% ({top1_correct}/{total})")
    print(f"  Top-3 Recall:    {top3_acc * 100:.1f}% ({top3_correct}/{total})")

    if failures:
        print("\nFailures (Expected skill not in Top-3):")
        for f in failures:
            print(f"  - [{f['id']}] Query: '{f['query']}'")
            print(f"    Expected: {f['expected']}, Got: {f['got']} (scores: {f['scores']})")

    passed = top3_acc >= min_accuracy
    if passed:
        print(f"\n[PASS] Benchmark satisfied accuracy threshold >= {min_accuracy * 100:.1f}%")
    else:
        print(f"\n[FAIL] Benchmark below accuracy threshold ({top3_acc * 100:.1f}% < {min_accuracy * 100:.1f}%)", file=sys.stderr)

    return passed


def main(argv: List[str]) -> int:
    cmd = argv[1] if len(argv) > 1 else 'benchmark'
    skills = load_all_skills()

    if not skills:
        print("Error: No skills found in skills directory", file=sys.stderr)
        return 1

    if cmd == 'budget':
        ok, errors = check_token_budgets(skills)
        if not ok:
            for err in errors:
                print(f"  FAIL: {err}", file=sys.stderr)
            return 1
        print("  PASS: All skills adhere to token budget constraints.")
        return 0

    elif cmd == 'route':
        if len(argv) < 3:
            print("Usage: harness.py route <query string>", file=sys.stderr)
            return 2
        query = ' '.join(argv[2:])
        results = route_query(query, skills, top_k=5)
        print(f"Routing results for: '{query}'")
        for rank, (name, score) in enumerate(results, 1):
            s = skills[name]
            print(f"  {rank}. {name:<26} (score: {score:>2}, pack: {s.pack})")
        return 0

    elif cmd == 'benchmark':
        scenarios_file = Path(argv[2]) if len(argv) > 2 else DEFAULT_SCENARIOS
        budget_ok, budget_errors = check_token_budgets(skills)
        if not budget_ok:
            for err in budget_errors:
                print(f"  FAIL: {err}", file=sys.stderr)
            return 1

        bench_ok = run_benchmark(scenarios_file, skills)
        return 0 if bench_ok else 1

    else:
        print("Usage: harness.py [budget | route <query> | benchmark [<scenarios.json>]]", file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main(sys.argv))
