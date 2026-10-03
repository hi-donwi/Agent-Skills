---
name: audit-logging
description: >-
  Build attributable business audit trails with append-only history, redaction, scoped access, retention, and durable mutation linkage. Use to prove who changed business state, not operational logs or behavioral analytics.
metadata:
  pack: core
  keywords: audit trail, business audit, append-only, actor attribution, before-after, impersonator, mutation history, tamper evidence, audit retention
---

# Business Audit Logging

## Overview
Make sensitive business changes attributable and recoverable without turning
audit history into a second unrestricted copy of confidential data.

## When to use
- Recording role changes, approvals, postings, exports, support impersonation, or configuration edits.
- Designing audit integrity, retention, restricted search, and evidence exports.

## Hand off when
| Need | Skill |
|---|---|
| Operational logging, traces, and alerts | `observability` |
| Behavioral events and funnels | `product-analytics` |
| Durable asynchronous dispatch | `background-jobs` |

## Process
1. Identify audited actions, required attribution, legal/business retention, reader
   roles, and failure policy. Do not assume every debug log is an audit record.
2. Define an immutable event ID, tenant/legal entity, original and effective actor,
   action, resource/version, outcome, timestamp, correlation, and sanitized change summary.
3. Redact secrets and unnecessary personal fields before persistence. Prefer changed
   field names and approved values/digests over unrestricted before/after snapshots.
4. Commit successful mutation history in the same transaction as the local mutation
   or a durable audit outbox. Failed attempts belong to a separate attributable event.
5. Restrict insert/read/delete privileges and separate administrative responsibilities.
   Append-only application behavior is not protection against database administrators;
   use protected anchors or immutable storage where the threat model requires it.
6. Scope queries and exports by current permissions. Record export access; minimize
   sensitive search fields and avoid logging audited payloads again in diagnostics.
7. Apply documented retention, holds, privacy restrictions, and controlled purge.
   Preserve non-sensitive integrity evidence without promising indefinite personal-data storage.
8. Test audit transport outages, rollback, retries, privileged changes, impersonation,
   tampering, redaction, and cross-tenant reads with synthetic records.

## Red flags
- Mutable history, sampled audit events, or audit insertion after an unprotected commit.
- Passwords/tokens in snapshots or effective actors hiding the original impersonator.
- Hash chains described as tamper-proof without an independently protected anchor.

## Verification
- Every required committed mutation has one attributable durable event.
- Rollbacks and transport outages follow the explicit failure policy.
- Redaction, reader isolation, integrity controls, retention, and holds are tested.

## References
- `references/audit-event-contract.md` - attribution and integrity boundaries.
