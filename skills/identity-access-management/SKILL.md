---
name: identity-access-management
description: >-
  Design identity federation, tenant-scoped RBAC/ABAC permissions, service credentials, and access revocation. Use for SSO, MFA, SCIM, or authorization models, not member benefit lifecycles or Quarkus-specific security wiring.
metadata:
  pack: core
  keywords: identity access, rbac, abac, sso, saml, oidc, mfa, scim, deprovisioning, directory removal, organization-scoped permissions, permission matrix, access revocation
---

# Identity and Access Management

## Overview
Separate authentication, active organization membership, resource permission,
and commercial entitlement. None of these implies the others.

## When to use
- Defining tenant-scoped roles, resource authorization, or enterprise federation.
- Revoking access after directory changes and managing scoped service credentials.

## Hand off when
| Need | Skill |
|---|---|
| Invitations, renewals, member eligibility, and benefits | `membership-management` |
| Quarkus sessions, Argon2id, and RolesAllowed | `quarkus-security` |
| AI tool execution permissions | `ai-tool-security` |

## Process
1. Inventory subjects, tenants/legal entities, resources, actions, and trust boundaries.
   Create an allow/deny matrix including outsiders and service identities; deny by default.
2. Verify identity with the established stack. For federation, validate issuer,
   audience, signature, replay defenses, callback state, and organization binding.
   Use maintained protocol libraries and the pinned provider contract.
3. Map identities by verified issuer and subject. Do not auto-link privileged accounts
   from matching email alone; define safe linking, recovery, MFA, and step-up policies.
4. Evaluate current membership plus role, resource ownership, and relevant attributes
   on the server for every sensitive action. Client navigation is never the authority.
5. Scope API/service credentials to tenant, actions, expiry, and rotation. Store them
   securely, reveal secrets only when necessary, and audit use without exposing values.
6. Define permission-cache and session revocation latency. Directory deprovisioning,
   owner changes, suspension, or compromised credentials must invalidate stale access.
7. Separate platform administration and tenant roles. Impersonation needs explicit
   authorization, bounded scope/time, visible attribution, and a business audit event.
8. Test horizontal/vertical escalation, forged scope, stale tokens, directory removal,
   account linking, recovery, and service credentials with synthetic principals.

## Red flags
- A global admin boolean, email-only SSO binding, or long-lived cached permissions.
- Treating authenticated users, paid subscribers, or tenant IDs as automatically authorized.
- Disabling access checks when identity infrastructure is unavailable.

## Verification
- The permission matrix passes for allowed and denied resource/action combinations.
- Revocation, federation failures, and account linking cannot bypass organization scope.
- Recovery and platform support flows have explicit auditable privileges.

## References
- `references/access-matrix.md` - permissions, federation, and revocation exercises.
