---
name: workflow-approvals
description: >-
  Build versioned human approval workflows, maker-checker controls, delegation, escalation, and atomic document transitions. Use for business approvals, not CI workflows, generic worker scheduling, or role definitions alone.
metadata:
  pack: core
  keywords: approval workflow, approver, maker-checker, self-approval, segregation of duties, delegation, escalation, submitted revision, document revision, approval policy
---

# Workflow and Approvals

## Overview
Approval authorizes a specific revision under a known policy. It does not grant
permanent privilege or remain valid when protected document facts change.

## When to use
- Implementing sequential/parallel approvals, independent checking, or exception review.
- Handling delegation, escalation, document amendments, and conflicting decisions.

## Hand off when
| Need | Skill |
|---|---|
| Identity, scoped roles, and current actor permissions | `identity-access-management` |
| Durable reminders and asynchronous side effects | `background-jobs` |
| Purchase-specific tolerances and matching | `erp-procurement` |
| CI workflow and pipeline gates | `ci-cd` |

## Process
1. Define states, allowed transitions, decision rules, thresholds, quorum, rejection,
   expiry, delegation, escalation, and segregation-of-duties constraints from the contract.
2. Version approval policies and snapshot the submitted document revision and route.
   Do not let live configuration silently rewrite in-flight approval obligations.
3. Recheck current actor eligibility, tenant/company scope, delegation bounds, and
   maker-checker constraints at decision time; frozen policy does not freeze permissions.
4. Record each decision immutably with actor, effective actor, policy/revision,
   reason, timestamp, and stable request key. Repeated decisions cannot count twice.
5. Transition the document atomically using expected state/version. Competing approve,
   reject, amend, and cancel requests must not produce contradictory committed outcomes.
6. Invalidate affected approvals when protected facts change; resubmit a new revision.
   Document narrowly allowed amendments rather than treating every edit identically.
7. Persist downstream effects and notification intentions durably. Do not keep database
   transactions open while waiting for humans; deadlines and reminders recheck current state.
8. Test self-approval through delegation, stale revisions, lost roles, quorum races,
   policy edits, replay, escalation, and cancellation with synthetic principals.

## Red flags
- Approving via a UI button without server checks or counting duplicate responses.
- Stale approvals authorizing changed amounts, or delegation bypassing maker-checker rules.
- Live policy changes altering in-flight routes without an explicit migration.

## Verification
- Only eligible independent actors can approve the exact submitted revision.
- Conflicting requests produce one valid transition and attributable decision history.
- Policy versioning, amendments, delegation, reminders, and replay are covered.

## References
- `references/approval-invariants.md` - policy/revision and concurrency exercises.
