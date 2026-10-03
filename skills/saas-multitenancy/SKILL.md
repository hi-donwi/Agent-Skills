---
name: saas-multitenancy
description: >-
  Enforce multi-tenant data isolation, trusted tenant context, row-level security, and noisy-neighbor limits. Use for shared customer infrastructure, not membership lifecycles or private agent context sharing.
metadata:
  pack: core
  keywords: multitenancy, multi-tenant, multi tenant, tenant isolation, tenant id, row-level security, rls, tenant context, noisy neighbor, cross-tenant, pooled connections
---

# SaaS Multi-Tenancy

## Overview

Make the tenant boundary enforceable across requests, persistence, asynchronous work,
and shared infrastructure. Authentication, membership, and isolation are separate checks.

## When to use

- Choosing pooled, schema, database, or infrastructure isolation for customer data.
- Preventing cross-tenant access in queries, caches, files, search, exports, and workers.
- Testing connection-pool reuse and per-tenant resource fairness.

## Hand off when

| Need | Skill |
|---|---|
| Invitations, member status, and owner transfer | `membership-management` |
| Tenant provisioning, suspension, and deletion | `saas-onboarding` |
| Private agent notes and context audiences | `context-privacy` |
| Quarkus persistence implementation | `quarkus-persistence` |

## Process

1. Classify global and tenant-owned data. Choose isolation from contractual residency,
   restore, scale, and operational requirements; document residual shared-service risks.
2. Resolve a requested tenant, then verify the authenticated actor's active membership
   or scoped service credential. A header, host, URL, or signed stale claim is not enough.
3. Propagate immutable verified scope explicitly or through a correctly bounded runtime
   context. Fail closed when missing; clear it after each request and worker execution.
4. Enforce scope on reads and writes, including raw SQL and bulk operations. In pooled
   schemas use scoped unique keys and composite foreign keys to prevent cross-tenant links.
5. For PostgreSQL RLS, use a restricted runtime role and transaction-local settings on
   the same connection. Check both USING and WITH CHECK; test privileged bypass separately.
6. Namespace caches, search filters, storage objects, signed downloads, and job payloads.
   Workers verify job ownership and current policy before constructing fresh context.
7. Apply aggregate tenant quotas, concurrency limits, and bounded queues; optional
   IP limits supplement rather than replace tenant-wide noisy-neighbor controls.
8. Test two tenants with colliding identifiers, absent and forged scope, reused
   connections, failed transactions, exports, and retries. Never use an admin role only.

## Red flags

- Treating RLS, database-per-tenant, or a tenant ID in a message as an absolute guarantee.
- Runtime roles with superuser, BYPASSRLS, ownership, or unnecessary privileged functions.
- Client-selected scope, unscoped foreign keys, or context surviving connection reuse.
- Assuming every identity must be duplicated per tenant instead of classifying global data.

## Verification

- Cross-tenant reads, writes, links, files, and exports are denied under the runtime role.
- Missing scope fails closed; connection and worker reuse never inherit another tenant.
- Per-tenant restore, throttling, and privileged administration have explicit boundaries.

## References

- `references/isolation-strategies.md` - isolation choices and transaction-safe RLS.
- `references/tenant-context.md` - verified scope across synchronous and asynchronous work.
