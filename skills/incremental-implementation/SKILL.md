---
name: incremental-implementation
description: Delivers changes incrementally. Use when implementing any feature or change that touches more than one file. Use when you're about to write a large amount of code at once, or when a task feels too big to land in one step. Do not use for single-file, single-function changes where the scope is already minimal.
metadata:
  pack: core
---

# Incremental Implementation

## Overview

Build in thin vertical slices — implement one piece, test it, verify it, then expand. Avoid implementing an entire feature in one pass. Each increment should leave the system in a working, testable state. This is the execution discipline that makes large features manageable.

## When to use
- Implementing any multi-file change
- Building a new feature from a task breakdown
- Refactoring existing code
- Any time you're tempted to write more than ~100 lines before testing

Do not use for single-file, single-function changes where the scope is already minimal.

## Process

```
Implement ──→ Test ──→ Verify ──→ Commit ──→ next slice
```

For each slice: implement the smallest complete piece, run tests (or write them), confirm the slice works, commit (`git-workflow`), then move on. Do not restart.

Prefer **vertical slices** (one complete path through the stack) over horizontal layers. Use contract-first slicing when backend and frontend must proceed in parallel. Tackle the riskiest unknown first.

Keep each increment one logical thing, compilable, independently revertable, and default-safe. Incomplete user-facing work ships behind a flag. Do not touch adjacent files "while you're here." Do not run the same build/test command twice on unchanged code.

Slicing examples, implementation rules, and agent prompts: `references/slicing.md`.

## Red flags
- More than 100 lines of code written without running tests
- Multiple unrelated changes in a single increment
- "Let me just quickly add this too" scope expansion
- Skipping the test/verify step to move faster
- Build or tests broken between increments
- Large uncommitted changes accumulating
- Building abstractions before the third use case demands it
- Touching files outside the task scope "while I'm here"
- Creating new utility files for one-time operations
- Running the same build/test command twice in a row without any intervening code change

## Verification

After completing all increments for a task:

- [ ] Each increment was individually tested and committed
- [ ] The full test suite passes
- [ ] The build is clean
- [ ] The feature works end-to-end as specified
- [ ] No uncommitted changes remain

Per-increment verification is the local check. Before declaring a task done, apply the project-wide Definition of Done as the final gate.

## References
- `references/slicing.md` — vertical/contract/risk slices, rules 0–5, increment checklist
