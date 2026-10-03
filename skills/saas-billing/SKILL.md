---
name: saas-billing
description: >-
  Implement recurring subscription billing, payment reconciliation, pricing, usage metering, and paid entitlements. Use for subscription economics, not member eligibility, ERP ledger posting, or general partner webhooks.
metadata:
  pack: core
  keywords: billing, subscription, stripe, paddle, recurring, entitlement, per-seat, usage metering, pricing tier, proration, dunning, premium
---

# SaaS Billing and Subscriptions

## Overview

Separate payment-provider facts, commercial subscription policy, and application
access. Retries, delayed events, and concurrent consumption must not create value twice.

## When to use

- Integrating payment providers (Stripe, LemonSqueezy, Paddle, Midtrans).
- Managing subscription states: trialing, active, past_due, unpaid, canceled.
- Handling payment and invoice webhooks reliably with signature validation and deduplication.
- Implementing flat-rate tiered, per-seat, or usage-based metered pricing models.
- Gating premium features and enforcing tenant quotas based on active subscriptions.

## Hand off when

| Need | Skill |
|---|---|
| Tenant data isolation and organization scoping | `saas-multitenancy` |
| Member eligibility, renewal, and owner transfer | `membership-management` |
| General partner webhook transport | `webhook-integrations` |
| REST endpoints, problem+json error formatting | `rest-api-contract` |
| API key auth, secret rotation, and HMAC defense | `security-hardening` |
| User-facing billing portals, pricing tables, UI states | `web-development` |

## Process

1. Define versioned prices, currency precision, billing account ownership, billable
   seats, trial policy, proration, tax inputs, refunds, and effective change times.
   Obtain jurisdictional requirements rather than inventing tax rules or grace periods.
2. Map provider customer and subscription IDs to verified tenants and environments.
   Use stable idempotency keys for checkout creation and other provider-side mutations.
3. Verify signatures and replay windows using the provider's supported mechanism and
   unmodified body. Bound input sizes and reject invalid deliveries before side effects.
4. Commit a deduplicated inbox and durable work record before acknowledging delivery.
   Duplicate pending events must remain recoverable; persistence failure is not success.
5. Serialize reconciliation per subscription. Providers may deliver snapshots out of
   order; fetch authoritative state when necessary rather than sorting by timestamps.
6. Evaluate paid capabilities independently of role permissions and release flags.
   Atomically reserve limited quota or seats; deduplicate consumption and corrections.
7. Derive effective access from explicit policy and provider state. Distinguish scheduled
   end-of-period cancellation from terminal cancellation; preserve billing/support access.
8. Reconcile provider totals periodically, monitor failed work, and test trial end,
   payment failure, retries, immediate cancellation, refunds, and concurrent quota use.

## Red flags

- Trusting client-side checkout redirects for order fulfillment instead of verified server webhooks.
- Processing webhooks non-idempotently, causing duplicated seat licenses or double balance credits.
- Hardcoding plan strings (`if (user.plan === "pro")`) scattered across business logic.
- Verifying webhooks against parsed JSON rather than raw incoming request body buffers.
- Locking customer accounts immediately upon the first transient payment failure.
- Acknowledging before durable capture, skipping pending duplicates, or trusting event order.
- Read-then-increment quota checks without concurrency protection or currency precision.

## Verification

- [ ] Webhook endpoint rejects invalid or missing provider-required signatures.
- [ ] Delivering the identical webhook payload twice results in single execution and idempotent 200 responses.
- [ ] Feature entitlement checks block unauthorized tenants with informative upgrade errors.
- [ ] Scheduled cancellation and immediate terminal cancellation follow distinct policies.
- [ ] Usage metering records events correctly and enforces configured quota thresholds.
- [ ] Out-of-order delivery, worker crashes, and concurrent usage cannot duplicate value.

## References

- `references/webhook-idempotency.md` - verified durable ingestion and reconciliation.
- `references/pricing-and-entitlements.md` - commercial policy and atomic quota handling.
