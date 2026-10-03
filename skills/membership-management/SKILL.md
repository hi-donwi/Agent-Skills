---
name: membership-management
description: >-
  Model organization or association memberships, invitations, eligibility, renewal, expiry, suspension, benefits, and ownership transfer. Use for member lifecycles, not login protocols, recurring payment processing, or tenant storage isolation.
metadata:
  pack: core
  keywords: membership, invitation, invite, member renewal, member expiry, eligibility, benefit, owner transfer, last owner, association, joining date, reactivation
---

# Membership Management

## Overview
A person, an organization membership, a commercial subscription, and a benefit
grant are different records with independent histories and authority.

## When to use
- Managing organization teams, associations, paid communities, or membership programs.
- Handling invitations, eligibility tiers, renewals, owner transfer, and benefit access.

## Hand off when
| Need | Skill |
|---|---|
| SSO, MFA, login, and permission enforcement | `identity-access-management` |
| Recurring charges, dunning, and billing entitlements | `saas-billing` |
| Tenant persistence isolation | `saas-multitenancy` |

## Process
1. Define whether membership means organization access, program eligibility, or both.
   Separate global identity, scoped membership, role assignments, and benefit grants.
2. Define states, effective dates, timezone, eligibility, tier changes, renewal windows,
   grace policy, expiry, suspension, cancellation, and reactivation from the domain contract.
3. Scope invitations to organization, verified recipient, grantable role, expiry, and
   inviter authority. Store token hashes; consume once atomically and never trust a form role.
   For existing members, apply an explicit merge/reactivation policy rather than
   silently replacing current roles or restoring access from an old invitation result.
4. Enforce membership uniqueness and authorized role changes. Transfer ownership
   atomically, preserving an active accountable owner under concurrent removals.
   Check all role/status-changing paths, including invitations, imports, directory
   synchronization, and suspension. Forced security revocation still blocks access;
   if no eligible owner remains, enter the explicit restricted recovery workflow.
5. Version membership terms and benefit eligibility. Derive active benefit access from
   current policy and dates, not one persistent active boolean or a successful payment alone.
6. Coordinate paid membership with verified billing outcomes using idempotent links.
   Define billable seats and pending invitations separately; payment cannot invent a role.
7. Revoke sessions, cached benefits, and scheduled work on suspension or departure.
   Renewal/expiry jobs must recheck current versions and handle late or repeated execution.
8. Audit lifecycle transitions and test replayed invites, identity mismatch, concurrent
   acceptance/removal, date boundaries, reactivation, and last-owner protection.

## Red flags
- One global member flag, raw invitation tokens in logs, or self-assigned owner roles.
- Treating payment status as authorization or removing the final owner concurrently.
- Invitation acceptance implicitly downgrading an existing owner without invariant checks.
- Extending renewal twice because a scheduler or payment callback was retried.

## Verification
- Membership, identity, billing, and benefits remain distinct and consistently scoped.
- Invitations and renewal events execute once; eligibility follows effective dates.
- Last-owner, suspension, and cached-access regressions have concurrency tests.

## References
- `references/membership-lifecycle.md` - lifecycle and ownership invariants.
