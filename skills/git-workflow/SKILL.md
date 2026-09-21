---
name: git-workflow
description: >-
  Use git well: atomic commits, clear messages, sensible branching, and clean
  PRs. Use when committing, branching, writing commit/PR messages, resolving
  conflicts, or structuring a change for review. Do not use for non-git VCS or for
  rewriting already-pushed shared history without explicit instruction.
metadata:
  pack: core
---

# Git Workflow & Versioning

## Overview

Small, atomic, well-described changes that are easy to review, revert, and bisect.

## When to use
- Committing work, opening a PR, or organizing a messy working tree.
- Writing commit/PR messages or resolving conflicts.

## Process
1. **Branch off the default branch** for any non-trivial change; never commit straight to it
   unless told to.
2. **Atomic commits** — one logical change each; don't mix refactor + feature + formatting.
3. **Conventional messages** — `type(scope): summary` (feat, fix, refactor, docs, test, chore),
   imperative mood, explain *why* in the body when non-obvious.
4. **Review your own diff** before committing (see `code-review`); never commit secrets,
   debug logging, or unrelated churn.
5. **Keep PRs small and focused;** describe intent, approach, and how it was verified.
6. **Commit/push only when asked.** Honor any required trailers/co-authors.

## Red flags
- Giant commits mixing many concerns; "wip"/"fix" messages with no context.
- Committing generated files, secrets, or `node_modules`.
- Force-pushing shared branches or rewriting public history without instruction.

## Verification
- Each commit builds and is self-contained; messages explain the change.
- The PR is scoped, described, and verified before review.

## Reference Index
- `references/expanded-guidance.md` — deeper branching, commit hygiene, PR review, conflict, and release versioning guidance.
