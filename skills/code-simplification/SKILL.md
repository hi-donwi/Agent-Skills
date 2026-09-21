---
name: code-simplification
description: Simplifies code for clarity. Use when refactoring code for clarity without changing behavior. Use when code works but is harder to read, maintain, or extend than it should be. Use when reviewing code that has accumulated unnecessary complexity. Do not use when changing behavior, fixing bugs, or adding features.
metadata:
  pack: core
---

# Code Simplification

> Inspired by the [Claude Code Simplifier plugin](https://github.com/anthropics/claude-plugins-official/blob/main/plugins/code-simplifier/agents/code-simplifier.md). Adapted here as a model-agnostic, process-driven skill for any AI coding agent.

## Overview

Simplify code by reducing complexity while preserving exact behavior. The goal is not fewer lines — it's code that is easier to read, understand, modify, and debug. Every simplification must pass a simple test: "Would a new team member understand this faster than the original?"

## When to use
- After a feature is working and tests pass, but the implementation feels heavier than it needs to be
- During code review when readability or complexity issues are flagged
- When you encounter deeply nested logic, long functions, or unclear names
- When refactoring code written under time pressure
- When consolidating related logic scattered across files
- After merging changes that introduced duplication or inconsistency

Do not use when the code is already readable, when you do not yet understand it, when a simpler version would be measurably slower in a performance-critical path, or when the module is about to be rewritten.

## Process
1. **Preserve behaviour exactly.** Same outputs, errors, side effects, and ordering. If you are not sure, do not change it. Tests must still pass without modification.
2. **Follow project conventions.** Match neighboring code; do not impose external style.
3. **Prefer clarity over cleverness.** Explicit beats compact when compact needs a mental pause.
4. **Understand before touching (Chesterton's Fence).** If you cannot say why the code exists, read more first.
5. **One simplification at a time.** Run tests after each change. Submit refactoring separately from features. If a pass would touch more than 500 lines, use automation rather than hand edits.
6. **Stay in scope.** Default to recently modified code. Unscoped simplification is churn.

Opportunity tables and language-specific examples: `references/simplification-patterns.md`.

## Red flags
- Simplification that requires modifying tests to pass (you likely changed behavior)
- "Simplified" code that is longer and harder to follow than the original
- Renaming things to match your preferences rather than project conventions
- Removing error handling because "it makes the code cleaner"
- Simplifying code you don't fully understand
- Batching many simplifications into one large, hard-to-review commit
- Refactoring code outside the scope of the current task without being asked

## Verification

After completing a simplification pass:

- [ ] All existing tests pass without modification
- [ ] Build succeeds with no new warnings
- [ ] Linter/formatter passes (no style regressions)
- [ ] Each simplification is a reviewable, incremental change
- [ ] The diff is clean — no unrelated changes mixed in
- [ ] Simplified code follows project conventions (checked against CLAUDE.md or equivalent)
- [ ] No error handling was removed or weakened
- [ ] No dead code was left behind (unused imports, unreachable branches)
- [ ] A teammate or review agent would approve the change as a net improvement
- [ ] Architecture classification is correct — extracted code lands in the right layer
  (Component / Hook / Utility / Service per `AGENTS.md` → Reusability Standards)

## References
- `references/simplification-patterns.md` — opportunity tables, language examples, rationalizations
