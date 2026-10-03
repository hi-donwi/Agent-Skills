---
name: webhook-integrations
description: >-
  Build inbound and outbound partner webhooks with authenticated payloads, durable delivery, endpoint validation, retries, and replay. Use for integration transport, not subscription reconciliation or general API design.
metadata:
  pack: core
  keywords: webhook, inbound, outbound, partner endpoint, signed payload, signature rotation, delivery receipt, dns rebinding, endpoint validation, https endpoint
---

# Webhook Integrations

## Overview
Treat webhook payloads and subscriber destinations as untrusted. Reliability
requires durable capture and effect-level idempotency, not merely returning 200.

## When to use
- Receiving partner events or delivering application events to tenant-configured endpoints.
- Implementing signing, endpoint validation, delivery history, and controlled replay.

## Hand off when
| Need | Skill |
|---|---|
| Payment/subscription state and paid access | `saas-billing` |
| Worker leases, outboxes, and generic effect recovery | `background-jobs` |
| Public API contracts and versioning | `api-design` |

## Process
1. Define direction, event schema/version, scope, provider account/environment,
   delivery identity, timeout, ordering contract, and authorized subscription management.
2. Verify incoming signatures against bounded unmodified bytes with the actual provider
   contract, replay window, and secret rotation. Do not trust tenant fields in the body.
3. Persist an authenticated event and durable pending work before acknowledging it.
   Deduplicate by scoped event ID and business effect; recover abandoned pending events.
4. Commit outbound event intentions with local mutations. Sign the exact transmitted
   bytes with a documented version, timestamp, event ID, and rotating endpoint secret.
5. Validate destinations against an approved HTTPS policy. Block private, loopback,
   link-local, metadata, and reserved addresses, including IPv6 and mapped addresses.
   Validate DNS at connection time, preserve TLS hostname checks, and disable redirects
   or revalidate each hop; registration-time checks alone do not stop SSRF.
6. Apply bounded retries, concurrency, response/body limits, redacted delivery records,
   and tenant fairness. Distinguish acceptance, business completion, and failed delivery.
7. Replay only with authorization and a stable event/effect identity. Do not invent
   event ordering; reconcile current state when late events may overwrite newer facts.
8. Test altered bytes, stale signatures, duplicate delivery, secret overlap, destination
   rebinding, redirects, persistence failure, provider outages, and worker crashes.

## Red flags
- Arbitrary URL fetching, automatic redirects, secrets in query strings, or raw-body logging.
- 2xx before durable persistence or timestamps treated as a guaranteed sequence.
- Replays creating new payment, inventory, or notification effects unintentionally.

## Verification
- Unauthenticated events and unsafe destinations are rejected before side effects.
- Accepted events remain recoverable and retries preserve one logical business result.
- Rotation, ordering, bounded delivery, and authorized replay have integration tests.

## References
- `references/delivery-contract.md` - signing, SSRF defense, and failure fixtures.
