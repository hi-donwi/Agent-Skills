# Audit Event Contract

## Required decisions

| Dimension | Contract |
|---|---|
| Identity | Original actor, effective actor, service identity, impersonation grant |
| Scope | Tenant/legal entity, resource identity and version, action |
| Time | UTC event and capture times; reliable clock and ordering conventions |
| Outcome | Committed, denied, or failed; sanitized reason; correlation ID |
| Changes | Allowlisted changed fields and approved values, not raw snapshots |
| Integrity | Mutation linkage, append permissions, protected archival/anchor policy |
| Lifecycle | Retention, legal hold, access restrictions, authorized export/purge |

Local mutation and audit/outbox insertion must share a commit boundary when audit is
required for correctness. Remote sink outages can leave durable pending work; local
persistence failure follows the declared fail-closed or explicitly approved alternative
policy. Do not silently drop or sample required evidence.

## Integrity limits

Application insert-only permissions reduce accidental edits but do not defeat a
database administrator. Hash chains can reveal modification only relative to a
trusted anchor and verification process; a compromised actor that rewrites both
history and anchor can still hide tampering. Document the threat model and controls.
Encryption at rest does not substitute for record-level access restrictions.

## Failure exercise

Disconnect the remote sink, perform a privileged mutation, and roll back another.
The committed mutation has one durable event; the rolled-back one is not represented
as committed. Retry dispatch without duplication. Include a password in the proposed
change; it is redacted before storage. Read from another tenant and attempt history
updates under the application role; both are denied.
