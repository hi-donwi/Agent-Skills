---
name: debugging
description: >-
  Systematically diagnose and fix failures instead of guessing. Use when facing a
  bug, stack trace, failing test, crash, or unexpected behavior, or when a fix
  attempt did not work. Do not use for greenfield design decisions with no defect
  to chase.
metadata:
  pack: core
---

# Debugging & Error Recovery

## Overview

Find the root cause before changing code. Random edits hide symptoms and create new bugs.

## When to use
- Any reproducible (or intermittent) defect, crash, or failing check.
- After a fix "didn't work" — reset and re-diagnose rather than pile on changes.

## Process
1. **Reproduce reliably** — get a minimal, deterministic repro. If flaky, find what varies.
2. **Read the actual error** — full message + stack trace; identify the first failing frame in
   your code, not the framework.
3. **Form one hypothesis** about the root cause and a cheap way to test it (log, breakpoint,
   bisect, or a failing test via `test-driven-development`).
4. **Test the hypothesis** — confirm or reject before editing. Change one variable at a time.
5. **Fix the cause, not the symptom.** Add a regression test that fails without the fix.
6. **Verify and clean up** — remove debug logging; confirm the original repro is gone and
   nothing nearby regressed.
7. **If the first fix failed** — do not stack patches. Revert to diagnosis; use
   `references/playbook.md` for bisect, isolation, and domain-specific recovery loops.

## Red flags
- Editing code before reproducing or reading the error.
- Multiple simultaneous changes so you can't tell what fixed it.
- "Fixes" that suppress the error (swallowed exceptions, broad try/catch) without understanding.
- No regression test after the fix.

## Verification
- The original repro now passes; a new test guards against regression.
- You can explain the root cause in one sentence.

## Reference Index
- `references/playbook.md` — flexible recovery when fixes fail, bisect tactics, scroll-video issues.
- `references/expanded-guidance.md` — deeper triage checklist, localization tactics, and recurrence prevention.
