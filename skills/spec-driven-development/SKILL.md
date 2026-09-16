---
name: spec-driven-development
description: Creates specs before coding. Use when starting a new project, feature, or significant change and no specification exists yet. Use when requirements are unclear, ambiguous, or only exist as a vague idea. Do not use when a spec already exists, or for small bugfixes that do not change intended behaviour.
metadata:
  pack: core
---

# Spec-Driven Development

## Overview

Write a structured specification before writing any code. The spec is the shared source of truth between you and the human engineer — it defines what we're building, why, and how we'll know it's done. Code without a spec is guessing.

## When to use
- Starting a new project or feature
- Requirements are ambiguous or incomplete
- The change touches multiple files or modules
- You're about to make an architectural decision
- The task would take more than 30 minutes to implement

Do not use for single-line fixes, typo corrections, or changes where requirements are unambiguous and self-contained. If a spec already exists, do not write another — implement against it.

## Process

Do not advance a phase until the current one is validated:

```
SPECIFY ──→ PLAN ──→ TASKS ──→ IMPLEMENT
```

1. **Specify.** Surface assumptions first. Cover objective, commands, project structure, code style, testing strategy, and boundaries (Always / Ask first / Never). Reframe vague requirements as testable success criteria. Spec template: `references/spec-template.md`.
2. **Plan.** Components, order, risks, parallel vs sequential, checkpoints. Canonical slicing lives in `planning-and-task-breakdown`. Save `tasks/plan.md` and `tasks/todo.md`.
3. **Tasks.** One focused session each, with acceptance criteria, verification, ≤ ~5 files, ordered by dependency.
4. **Implement** with `incremental-implementation` and `test-driven-development`. Load the right spec sections via `context-engineering`.
5. **Keep the spec alive.** Update it when decisions or scope change; commit it; link it from PRs.

## Red flags
- Starting to write code without any written requirements
- Asking "should I just start building?" before clarifying what "done" means
- Implementing features not mentioned in any spec or task list
- Making architectural decisions without documenting them
- Skipping the spec because "it's obvious what to build"

## Verification

Before proceeding to implementation, confirm:

- [ ] The spec covers all six core areas
- [ ] The human has reviewed and approved the spec
- [ ] Success criteria are specific and testable
- [ ] Boundaries (Always/Ask First/Never) are defined
- [ ] The spec is saved to a file in the repository

## References
- `references/spec-template.md` — six-area spec, assumption list, success-criteria reframe
