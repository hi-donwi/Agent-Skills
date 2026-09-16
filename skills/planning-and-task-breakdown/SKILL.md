---
name: planning-and-task-breakdown
description: Breaks work into ordered tasks. Use when you have a spec or clear requirements and need to break work into implementable tasks. Use when a task feels too large to start, when you need to estimate scope, or when parallel work is possible. Do not use when requirements are still unclear (spec-driven-development) or when the work is already a single small task.
metadata:
  pack: core
---

# Planning and Task Breakdown

## Overview

Decompose work into small, verifiable tasks with explicit acceptance criteria. Good task breakdown is the difference between an agent that completes work reliably and one that produces a tangled mess. Every task should be small enough to implement, test, and verify in a single focused session.

## When to use
- You have a spec and need to break it into implementable units
- A task feels too large or vague to start
- Work needs to be parallelized across multiple agents or sessions
- You need to communicate scope to a human
- The implementation order isn't obvious

Do not use for single-file changes with obvious scope, or when the spec already contains well-defined tasks. If requirements are still unclear, use `spec-driven-development`.

## Process
1. **Plan read-only.** Read the spec and codebase. Map dependencies and risks. Do not write implementation. Output `tasks/plan.md` and `tasks/todo.md`.
2. **Order by the dependency graph, then slice vertically.** One complete feature path at a time, not "all schema then all API then all UI."
3. **Write S/M tasks** with acceptance criteria, a verification step, dependencies, and likely files. L/XL tasks get broken down. Checkpoints after every 2–3 tasks. High-risk work first.
4. **Parallelize only independent slices.** Migrations, shared state, and dependency chains stay sequential. Shared API contracts are defined first, then parallelized.

Task template, sizing table, and plan document: `references/task-templates.md`.

## Red flags
- Starting implementation without a written task list
- Tasks that say "implement the feature" without acceptance criteria
- No verification steps in the plan
- All tasks are XL-sized
- No checkpoints between tasks
- Dependency order isn't considered

## Verification

Before starting implementation, confirm:

- [ ] Every task has acceptance criteria
- [ ] Every task has a verification step
- [ ] Task dependencies are identified and ordered correctly
- [ ] No task touches more than ~5 files
- [ ] Checkpoints exist between major phases
- [ ] The human has reviewed and approved the plan

Acceptance criteria answer "did we build the right thing?". They sit on top of the project-wide Definition of Done.

## References
- `references/task-templates.md` — task card, sizing, plan document, parallelization
