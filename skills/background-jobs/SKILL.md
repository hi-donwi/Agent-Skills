---
name: background-jobs
description: >-
  Build durable background jobs, scheduled tasks, transactional outboxes, retries, leases, and dead-letter recovery. Use for asynchronous business effects, not CI pipelines or frontend async state.
metadata:
  pack: core
  keywords: background job, scheduled task, scheduler, outbox, worker, lease, fencing, retry, dead-letter, replay, external side effect
---

# Background Jobs and Durable Effects

## Overview
Persist the intention before dispatch and make repeated delivery safe. Broker
acknowledgment is not proof that a business effect happened exactly once.

## When to use
- Adding workers, recurring tasks, durable dispatch, retries, or crash recovery.
- Coordinating database commits and asynchronous external side effects.

## Hand off when
| Need | Skill |
|---|---|
| HTTP delivery signatures and partner endpoint safety | `webhook-integrations` |
| Human approval policy and document revisions | `workflow-approvals` |
| Pipeline jobs and automated build gates | `ci-cd` |

## Process
1. Define job identity, scope, initiator, payload version, operation key, timeout,
   retry budget, cancellation, ordering, and the business completion condition.
2. Commit the job or outbox with the initiating local mutation. Use a durable existing
   mechanism; do not introduce a broker or paid service solely because this skill loaded.
3. Claim work atomically with a lease and incarnation/fencing token. Renew or expire
   ownership explicitly; a recovered worker must not accept a former owner's commit.
4. Deduplicate each business effect with stable operation keys. For external systems,
   use supported idempotency or reconcile uncertain results before sending again.
5. Reconstruct verified tenant context and current permissions/lifecycle in workers.
   Payload fields are not authority; cap per-tenant concurrency and resource consumption.
6. Retry only transient failures with bounded backoff and jitter. Preserve attempt
   history; dead-letter permanent or exhausted work and expose an authorized recovery path.
7. Specify recurrence timezone, daylight-saving behavior, overlap, missed runs, and
   a stable occurrence key. Catch-up must not bill, renew, or notify twice.
8. Monitor queue age, completion latency, failed attempts, and abandoned leases.
   Test crashes before/after effects, dispatch loss, stale workers, cancellation, and replay.

## Red flags
- Best-effort publish after commit, unbounded retries, or acknowledgment before durable state.
- Treating deduplicated messages as deduplicated external effects.
- Replaying dead-letter work without checking current authority or payload compatibility.

## Verification
- Every committed intent is recoverable; duplicate attempts produce one business result.
- Stale workers cannot commit and uncertain external outcomes have reconciliation.
- Scheduling, cancellation, tenant fairness, and dead-letter replay are tested.

## References
- `references/durable-execution.md` - crash boundaries and recovery contracts.
