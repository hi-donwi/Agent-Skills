---
name: feature-flags
description: >-
  Manage release toggles, deterministic targeting, percentage rollouts, kill switches, and flag retirement. Use to separate deployment from exposure, not to replace paid entitlements or authorization.
metadata:
  pack: core
  keywords: feature flag, release toggle, targeting, percentage rollout, kill switch, kill-switch, flag debt, canary, cohort, flag provider
---

# Feature Flags

## Overview
Control exposure without turning release configuration into a security boundary.
Flag failures, stale rules, and cleanup need explicit policies.

## When to use
- Releasing gradually, targeting verified tenant cohorts, or running an experiment.
- Adding an operational kill switch or retiring temporary release toggles.

## Hand off when
| Need | Skill |
|---|---|
| Commercial feature access and usage limits | `saas-billing` |
| Role and resource authorization | `identity-access-management` |
| Complete production release readiness | `shipping-and-launch` |
| Experiment events and metric definitions | `product-analytics` |

## Process
1. Classify each flag as release, experiment, or operational. Record owner, scope,
   expected lifetime, default, cleanup condition, and dependencies before adding it.
2. Evaluate using verified context and stable targeting keys. Tenant-wide behavior
   needs tenant cohorts, not random per-request choices or unverified email domains.
3. Keep evaluation bounded using supported local rules or a documented bounded remote
   strategy. Define initialization, cache staleness, provider outages, and per-flag fallback.
4. Enforce authorization and paid capabilities separately on the server. Browser
   variants are presentation only; do not expose sensitive targeting rules to clients.
5. Test both branches, cohort boundaries, empty context, stale configuration, and
   outages. Keep assignment consistent across services that implement the same decision.
6. Define rollout stages and measurable hold/rollback criteria. Audit configuration
   changes and verify kill-switch propagation time rather than assuming instant effect.
7. Retire release flags after all deployed versions no longer need the old path.
   Remove code before deleting remotely used definitions; retain deliberate operational flags.

## Red flags
- Random reassignment, plan names in targeting rules, or flags used as authorization.
- A universal false fallback that accidentally disables a protective kill switch.
- Permanent release debt or remote deletion while older application versions still run.

## Verification
- Assignment is deterministic and isolated by tenant where required.
- Outages and stale rules follow tested per-flag policy; access checks still apply.
- Rollback propagation and retirement are verified across deployed versions.

## References
- `references/evaluation-patterns.md` - local evaluation and stable assignment.
- `references/flag-lifecycle.md` - ownership, rollout, and retirement.
