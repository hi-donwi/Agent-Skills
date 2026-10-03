---
name: saas-onboarding
description: >-
  Build tenant provisioning, activation, suspension, offboarding, and deletion workflows. Use for organization lifecycle and recovery, not repository onboarding, member renewals, or subscription pricing.
metadata:
  pack: core
  keywords: tenant provisioning, organization provisioning, tenant lifecycle, activation checklist, offboarding, deprovision, retention hold, deletion manifest
---

# SaaS Onboarding and Tenant Lifecycle

## Overview
Provision and retire organizations through resumable, authorized transitions.
The lifecycle must govern access and workers, not just a welcome screen.

## When to use
- Creating tenants, seeding configuration, verifying domains, or tracking activation.
- Suspending, restoring, exporting, or deleting an organization's data and integrations.

## Hand off when
| Need | Skill |
|---|---|
| Learning an unfamiliar repository | `codebase-onboarding` |
| Member invitations, eligibility, and owner transfer | `membership-management` |
| Persistence isolation and trusted tenant context | `saas-multitenancy` |
| Commercial subscription state | `saas-billing` |

## Process
1. Define states and allowed transitions such as requested, provisioning, active,
   suspended, deletion-pending, and deleted. Keep billing and activation progress distinct.
2. Authenticate the requester, validate reserved identifiers and ownership, and create
   an idempotent provisioning record. Establish the first owner atomically with scope.
3. Persist provisioning steps and effect keys. Retry only unfinished steps; never
   activate a partially configured tenant or duplicate external customer resources.
4. Verify custom-domain control and unique mapping before routing traffic. Document
   DNS propagation, certificate issuance, expiry, and takeover prevention on removal.
5. Apply lifecycle checks at requests, credentials, scheduled work, and integrations.
   Suspension invalidates stale access and fences provisioning or background retries.
6. Before offboarding, verify authority and the approved export, retention, hold,
   cancellation, and deletion policy. Do not run destructive operations without authorization.
7. Track deletion across databases, files, search, caches, analytics, and integrations.
   Record backup expiry and restoration suppression; do not promise immediate backup erasure.
8. Define recovery objectives and test a tenant-scoped restore without overwriting
   other tenants, duplicating effects, or resurrecting previously deleted data.

## Red flags
- Boolean active flags with no resumable provisioning or auditable transition history.
- Domain ownership assumed from a submitted host or retries reviving suspended tenants.
- Deleting held records, silently retaining integrations, or claiming backups are purged.

## Verification
- Repeated signup and step failures provision one complete tenant only.
- Suspension and deletion block stale sessions, workers, domains, and service credentials.
- Export, hold enforcement, restore isolation, and deletion manifests are verified.

## References
- `references/lifecycle-checklist.md` - transition contracts and recovery exercises.
