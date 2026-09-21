---
name: ci-cd
description: >-
  Set up or improve CI/CD pipelines: automated lint/test/build gates, safe
  deployments, and fast feedback. Use when adding GitHub Actions (or similar),
  defining quality gates, fixing a failing pipeline, or designing a release/rollout.
  Do not use for application feature logic unrelated to the pipeline.
metadata:
  pack: core
---

# CI/CD & Automation

## Overview

Automate the checks and the release so quality is enforced and shipping is boring.

## When to use
- Creating/maintaining a CI pipeline or deployment workflow.
- Adding quality gates; debugging a red build; designing a rollout.

## Process
1. **Shift left** — run the fastest, most decisive checks first: lint → unit tests → build →
   integration/e2e → perf/security gates. Fail fast.
2. **Make it reproducible** — pinned versions, clean environment, cached deps; no machine-specific
   assumptions.
3. **Gate merges** on the pipeline; keep the default branch always releasable.
4. **Deploy safely** — automate releases; use staged/canary rollouts and feature flags for risky
   changes; ensure a fast rollback path.
5. **Keep it fast** — parallelize, cache, and split slow suites so feedback stays quick.
6. **Debug failures** from the actual logs (see `debugging`); reproduce locally before "fix CI"
   commits.

## Red flags
- Flaky tests left red or retried blindly until green.
- Secrets in workflow files instead of the CI secret store.
- Deploys with no rollback plan; big-bang releases of risky changes.
- Slow pipelines that push people to bypass them.

## Verification
- The pipeline blocks merges on failure and passes deterministically.
- A release can be rolled back quickly; risky changes ship behind a flag.

## Reference Index
- `references/expanded-guidance.md` — deeper CI/CD pipeline design, quality gates, deployment, and automation guidance.
