---
name: codebase-onboarding
description: >-
  Build a concise mental model of an unfamiliar repository: architecture, entry
  points, workflows, ownership hotspots, tests, risks, and next files to read.
  Use when starting work in an unknown or large codebase, before major refactors,
  or when asked to explain how a project works. Do not use for tiny edits in
  already-understood code.
metadata:
  pack: core
---

# Codebase Onboarding

Learn the shape of the codebase before changing it.

## When to Use

- New repository, unfamiliar module, large refactor, or architecture question.
- You need to identify entry points, ownership boundaries, or risky files.
- A task requires understanding before implementation.

## Process

1. **Map the repo quickly.** List top-level directories, package manifests,
   build files, test config, and docs.
2. **Find entry points.** App routes, server startup, CLI commands, workers,
   jobs, public APIs, schemas, and generated code boundaries.
3. **Use history when useful.** `git log`, churn, recent commits, and blame can
   reveal hotspots and bug-prone files.
4. **Trace one real flow.** Follow a representative request/user action from
   entry point to output/storage.
5. **Identify local conventions.** Naming, error handling, dependency injection,
   testing style, state management, and folder ownership.
6. **Produce an onboarding map.** Include architecture summary, key files,
   commands, risks, and recommended next reads.

## Red Flags

- Editing before identifying the owning module and tests.
- Treating generated/vendor/build output as source.
- Ignoring docs or scripts that define local commands.
- Summaries with no file references.

## Verification

- The onboarding output names real files and commands.
- At least one representative flow was traced.
- Risks and unknowns are explicit.
