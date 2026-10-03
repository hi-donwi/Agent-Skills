# Webhook Security and Idempotent Ingestion

## 1. Cryptographic Signature Verification

Capture a bounded unmodified body and verify it before interpreting it or executing
logic. Use the installed provider SDK and pinned API contract, not an invented SDK
version. Signature formats differ across providers. Check supported replay windows,
secret rotation, endpoint/account mapping, and production versus test environments.
Return a generic validation error; do not log secrets, bodies, or SDK error details.

[Stripe webhook documentation](https://docs.stripe.com/webhooks) requires raw bytes,
documents duplicate delivery, and explicitly provides no event-order guarantee.

## 2. Idempotency and Deduplication Pattern

Payment providers resend webhooks on transient errors or timeouts. A reliable billing system must treat duplicate webhook deliveries as harmless no-ops.

### Database Schema for Ingestion Tracking

```sql
CREATE TABLE webhook_events (
  id VARCHAR(255) NOT NULL,
  provider VARCHAR(64) NOT NULL, -- 'stripe', 'lemonsqueezy', 'paddle'
  provider_account VARCHAR(255) NOT NULL,
  environment VARCHAR(16) NOT NULL,
  event_type VARCHAR(128) NOT NULL,
  status VARCHAR(32) NOT NULL DEFAULT 'processing', -- 'processing', 'completed', 'failed'
  payload JSONB NOT NULL,
  attempts INT NOT NULL DEFAULT 1,
  error_message TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  processed_at TIMESTAMPTZ,
  PRIMARY KEY (provider, provider_account, environment, id)
);

CREATE INDEX idx_webhook_status ON webhook_events (provider, status);
```

### Ingestion Flow

1. **Atomic Insertion:** Attempt to insert the event into `webhook_events`.
   ```sql
    INSERT INTO webhook_events (id, provider, provider_account, environment, event_type, payload)
    VALUES ($1, $2, $3, $4, $5, $6)
    ON CONFLICT (provider, provider_account, environment, id) DO NOTHING;
   ```
2. **Recoverable Duplicate:** A duplicate may return 2xx only when already completed
   or covered by durable pending work. Failed or abandoned processing needs retry or
   reconciliation; a unique event ID alone does not guarantee completion.
3. **Execution Boundary:** Execute the state change (e.g. updating customer plan) inside a database transaction alongside marking the event `'completed'`.
4. **Fast Acknowledgment:** Commit the inbox and a durable job/outbox atomically, or
   poll the inbox as the durable queue. A best-effort publish after commit can lose
   work. Return retryable failure when persistence fails.
5. **Ordering:** Serialize work per mapped subscription and reconcile authoritative
   provider state using the correct account context. Event timestamps can collide;
   do not use them as a guaranteed sequence. Business effects also need stable keys
   when two distinct event IDs describe the same payment or invoice.
6. **Retention:** Encrypt and minimize stored payloads, redact errors, scope access,
   and define expiry. Payload retention need not equal financial record retention.

## Failure exercise

Deliver an active snapshot after a terminal cancellation, retry an existing pending
event, and crash between capture and dispatch. Access must not regress, pending work
must remain recoverable, and the same payment must never grant a second credit.
