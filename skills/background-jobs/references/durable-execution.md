# Durable Execution Contract

## Crash boundaries

| Boundary | Required recovery |
|---|---|
| Mutation committed, dispatch absent | Poll durable job/outbox and dispatch later |
| Message delivered twice | Claim or deduplicate the logical operation |
| Worker lease expires during work | Reject stale commit with ownership/version check |
| External effect succeeds, local result absent | Provider idempotency or authoritative reconciliation |
| Local effect committed, acknowledgment lost | Repeated attempt observes completed operation |
| Permanently invalid payload | Dead-letter with sanitized reason and authorized remediation |

Store job ID, tenant, initiating actor/service, payload version, operation key,
status, attempt count, available time, lease owner/expiry, fencing version, and result
reference. Do not store credentials in payloads; resolve protected credentials at execution.
Encrypt/minimize payload data and apply a retention policy to attempts and dead letters.

A uniqueness constraint on operation keys protects local effects only when checked
in the same transaction as the effect. A fencing token protects a resource only when
that resource validates it. It cannot undo an email, charge, or arbitrary remote call.

## Retry and scheduling policy

Classify failures explicitly. Configuration, authorization, and invalid data errors
need correction, not endless retries. Respect upstream rate limits and per-tenant
budgets. Cancellation is a versioned transition with defined points after which
compensation may be required. Long work checks cancellation and ownership periodically.
Scheduled occurrences use explicit timezone and logical occurrence IDs; decide
whether missed occurrences are skipped, coalesced, or caught up with a bounded limit.

## Failure exercise

Kill a worker after an external effect succeeds but before local completion. Restart,
deliver twice, then let the old lease holder return. One logical effect remains,
reconciliation resolves ambiguity, and only the current incarnation may commit.
This requires a controlled fake provider and database tests in the implementing project.
