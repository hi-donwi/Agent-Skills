# Tenant Lifecycle Checklist

## Transition contract

Record the tenant ID, current and expected state/version, authorized initiator,
transition ID, timestamps, reason, and durable steps. Competing transitions require
a compare-and-set or lock; a provisioning worker must not overwrite suspension.

| Stage | Required boundary |
|---|---|
| Requested | Validated owner, identifier uniqueness, abuse controls, idempotency |
| Provisioning | Durable step status; explicit retry and compensation policy |
| Active | Required resources ready; current owner and scoped permissions exist |
| Suspended | Access and new work blocked; recovery/support exceptions explicit |
| Deletion-pending | Authority, export, approved retention and holds checked |
| Deleted | Live-system manifest complete; domain mapping removed; restore suppression |

Use a durable outbox or job record for provisioning side effects. If an external
provider cannot deduplicate creation, persist its request identity and reconcile
before retrying. Compensation must not destroy shared resources or held records.

## Deletion and recovery

Keep a restricted deletion manifest naming systems and completion states, not raw
customer data. Track legal holds separately from access suspension. Data retained for
financial or legal requirements is restricted, not available for ordinary product use.
When immutable backups cannot be selectively erased, document expiry and maintain a
minimal suppression record so restores reapply deletion before reopening access.

## Failure exercise

Crash after external resource creation, then retry signup. Resume one resource, not
two. Suspend while provisioning runs and initiate deletion with a retention hold.
Late workers must fail the lifecycle fence; held records remain restricted. Restore
one tenant into a controlled environment and confirm no other tenant is overwritten.
