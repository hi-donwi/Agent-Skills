---
name: deprecation-and-migration
description: Manages deprecation and migration. Use when removing old systems, APIs, or features. Use when migrating users from one implementation to another. Use when deciding whether to maintain or sunset existing code. Do not use for ordinary refactors that keep the same public contract, or for git history rewrites.
metadata:
  pack: core
---

# Deprecation and Migration

## Overview

Code is a liability, not an asset. Every line of code has ongoing maintenance cost — bugs to fix, dependencies to update, security patches to apply, and new engineers to onboard. Deprecation is the discipline of removing code that no longer earns its keep, and migration is the process of moving users safely from the old to the new.

Most engineering organizations are good at building things. Few are good at removing them. This skill addresses that gap.

## When to use
- Replacing an old system, API, or library with a new one
- Sunsetting a feature that's no longer needed
- Consolidating duplicate implementations
- Removing dead code that nobody owns but everybody depends on
- Planning the lifecycle of a new system (deprecation planning starts at design time)
- Deciding whether to maintain a legacy system or invest in migration

Do not use for ordinary refactors that keep the same public contract, or for git history rewrites.

## Process
1. **Decide.** Unique value still? How many consumers? Replacement exists? Migration cost vs 2–3 years of maintenance? Default to advisory deprecation; compulsory only when risk or cost forces a deadline.
2. **Build the replacement first.** Cover critical use cases, document it, prove it in production.
3. **Announce with a migration guide.** You own the churn: migrate consumers or provide a backward-compatible shim. Do not announce and walk away.
4. **Migrate incrementally** (strangler, adapter, or feature flag). Then remove only after metrics show zero usage.

Principles, notice template, and patterns: `references/migration-patterns.md`.

## Red flags
- Deprecated systems with no replacement available
- Deprecation announcements with no migration tooling or documentation
- "Soft" deprecation that's been advisory for years with no progress
- Zombie code with no owner and active consumers
- New features added to a deprecated system (invest in the replacement instead)
- Deprecation without measuring current usage
- Removing code without verifying zero active consumers

## Verification

After completing a deprecation:

- [ ] Replacement is production-proven and covers all critical use cases
- [ ] Migration guide exists with concrete steps and examples
- [ ] All active consumers have been migrated (verified by metrics/logs)
- [ ] Old code, tests, documentation, and configuration are fully removed
- [ ] No references to the deprecated system remain in the codebase
- [ ] Deprecation notices are removed (they served their purpose)

## References
- `references/migration-patterns.md` — decision questions, notice, strangler/adapter/flag, zombies
