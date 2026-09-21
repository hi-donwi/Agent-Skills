---
name: shipping-and-launch
description: Prepares production launches. Use when preparing to deploy to production. Use when you need a pre-launch checklist, when setting up monitoring, when planning a staged rollout, or when you need a rollback strategy. Do not use for CI pipeline setup (ci-cd) or for writing the production code being launched.
metadata:
  pack: core
---

# Shipping and Launch

## Overview

Ship with confidence. The goal is not just to deploy — it's to deploy safely, with monitoring in place, a rollback plan ready, and a clear understanding of what success looks like. Every launch should be reversible, observable, and incremental.

## When to use
- Deploying a feature to production for the first time
- Releasing a significant change to users
- Migrating data or infrastructure
- Opening a beta or early access program
- Any deployment that carries risk (all of them)

Do not use for CI pipeline setup (`ci-cd`) or for writing the production code being launched.

## Process
1. **Clear the pre-launch checklists** (code quality, security, performance, accessibility, infrastructure, documentation) in `references/launch-playbook.md`.
2. **Ship behind a feature flag.** Deploy with the flag off, then enable for team → canary → gradual → 100%. Every flag has an owner and an expiration. Clean up within two weeks of full rollout. Do not nest flags. Test both states in CI.
3. **Advance only on green thresholds.** Error rate within 10% of baseline, p95 latency within 20%, no new client error types. Hold or roll back using the table in the playbook.
4. **Watch the first hour.** Health 200, no new error types, latency unchanged, critical flow works, logs flowing, rollback ready.
5. **Have a rollback plan before deploy.** Flag off in under a minute beats a revert. Know the database story (preserve vs clean up) before you need it.

## Red flags
- Deploying without a rollback plan
- No monitoring or error reporting in production
- Big-bang releases (everything at once, no staging)
- Feature flags with no expiration or owner
- No one monitoring the deploy for the first hour
- Production environment configuration done by memory, not code
- "It's Friday afternoon, let's ship it"

## Verification

Before deploying:

- [ ] Pre-launch checklist completed (all sections green)
- [ ] Feature flag configured (if applicable)
- [ ] Rollback plan documented
- [ ] Monitoring dashboards set up
- [ ] Team notified of deployment

After deploying:

- [ ] Health check returns 200
- [ ] Error rate is normal
- [ ] Latency is normal
- [ ] Critical user flow works
- [ ] Logs are flowing
- [ ] Rollback tested or verified ready

## References
- `references/launch-playbook.md` — checklists, flags, staged rollout, monitoring, rollback plan
- Workspace `definition-of-done` — apply it first
- `security-hardening`, `performance-optimization`, `frontend-ui-engineering/references/production-ui-checklist.md` for the matching pre-launch slices
