---
name: test-driven-development
description: Drives development with tests. Use when implementing any logic, fixing any bug, or changing any behavior. Use when you need to prove that code works, when a bug report arrives, or when you're about to modify existing functionality. Do not use for documentation-only edits, or for browser e2e verification (webapp-testing).
metadata:
  pack: core
---

# Test-Driven Development

## Overview

Write a failing test before writing the code that makes it pass. For bug fixes, reproduce the bug with a test before attempting a fix. Tests are proof — "seems right" is not done. A codebase with good tests is an AI agent's superpower; a codebase without tests is a liability.

## When to use
- Implementing any new logic or behavior
- Fixing any bug (the Prove-It Pattern)
- Modifying existing functionality
- Adding edge case handling
- Any change that could break existing behavior

Do not use for pure configuration, documentation, or static content with no behavioral impact. For browser journeys, combine TDD with `webapp-testing`.

## Process

```
    RED                GREEN              REFACTOR
 Write a test    Write minimal code    Clean up the
 that fails  ──→  to make it pass  ──→  implementation  ──→  (repeat)
      │                  │                    │
      ▼                  ▼                    ▼
   Test FAILS        Test PASSES         Tests still PASS
```

1. **RED** — Write a test that fails. A test that passes immediately proves nothing.
2. **GREEN** — Write the minimum code to make it pass. Do not over-engineer.
3. **REFACTOR** — Improve structure without changing behaviour. Re-run tests after every refactor step.
4. **Prove-it for bugs.** Do not start with a fix. Write a test that reproduces the bug (it must fail), then fix, then confirm the test passes and the suite is green.
5. **Invest in small tests.** Most coverage should be unit tests; integration next; E2E only for critical paths. Patterns, pyramid, and anti-patterns: `references/test-patterns.md`.

Do not repeat the same test command on unchanged code. Run again only after the code has changed.

## Red flags
- Writing code without any corresponding tests
- Tests that pass on the first run (they may not be testing what you think)
- "All tests pass" but no tests were actually run
- Bug fixes without reproduction tests
- Tests that test framework behavior instead of application behavior
- Test names that don't describe the expected behavior
- Skipping tests to make the suite pass
- Running the same test command twice in a row without any intervening code change

## Verification

After completing any implementation:

- [ ] Every new behavior has a corresponding test
- [ ] All tests pass: `npm test`
- [ ] Bug fixes include a reproduction test that failed before the fix
- [ ] Test names describe the behavior being verified
- [ ] No tests were skipped or disabled
- [ ] Coverage hasn't decreased (if tracked)

## References
- `references/test-patterns.md` — pyramid, DAMP, doubles, anti-patterns, browser DevTools, subagents
- `webapp-testing/references/devtools-mcp.md` — runtime verification in a real browser
