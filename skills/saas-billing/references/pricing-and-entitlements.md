# Pricing Models and Entitlement Architecture

## 1. SaaS Pricing Archetypes

| Model | Mechanics | Metering & Invoicing | Example Products |
|---|---|---|---|
| **Flat-Rate Tiered** | Fixed fee per interval (Free / Pro / Business) granting static capabilities. | Recurring charge at period start. Simple invoicing. | Basecamp, Linear standard |
| **Seat-Based (Per-User)** | Cost scales with active team members (`$15/seat/month`). | Prorated charges on seat addition; credits on seat removal. | Slack, GitHub, Figma |
| **Usage-Based (Metered)** | Cost scales directly with consumption (API calls, storage GB, tokens, events). | Invoiced in arrears at period end based on reported usage meters. | AWS, Stripe, Twilio |
| **Hybrid** | Base subscription fee (includes quota of N units) + metered overage rate. | Base billed in advance; overages calculated and billed in arrears. | Datadog, Vercel |

## 2. Decoupled Entitlement Architecture

Never hardcode plan names like `if (user.plan === "enterprise")` throughout your application code. Plans change; capabilities evolve. Instead, decouple **Plans** from **Entitlements / Features**.

### Schema Pattern

```sql
-- Feature definition
CREATE TABLE features (
  key VARCHAR(64) PRIMARY KEY, -- 'custom_domain', 'sso_saml', 'audit_logs', 'api_calls'
  type VARCHAR(32) NOT NULL,    -- 'boolean' or 'metered_quota'
  description TEXT
);

-- Plan definition
CREATE TABLE plans (
  id VARCHAR(64) PRIMARY KEY, -- 'plan_starter', 'plan_growth', 'plan_enterprise'
  name VARCHAR(64) NOT NULL,
  provider_price_id VARCHAR(128)
);

-- Plan capabilities mapping
CREATE TABLE plan_entitlements (
  plan_id VARCHAR(64) REFERENCES plans(id),
  feature_key VARCHAR(64) REFERENCES features(key),
  quota_limit BIGINT, -- NULL for boolean features; numeric ceiling for metered
  PRIMARY KEY (plan_id, feature_key)
);
```

### Authorization Check

```typescript
export async function assertEntitlement(tenantId: string, featureKey: string): Promise<void> {
  const entitlement = await getTenantEntitlement(tenantId, featureKey);

  if (!entitlement || !entitlement.enabled) {
    throw new EntitlementError(`Feature '${featureKey}' is not enabled on your current subscription plan`);
  }

  // This checks capability only. Limited operations require atomic quota reservation.
}
```

For limited operations, atomically reserve the requested quantity against the
period's remaining quota, keyed by tenant, feature, period, and operation ID. Commit
the reservation with local work; for external effects use a durable workflow and
release or reconcile abandoned reservations. A read-then-increment permits overspend.
Record corrections rather than silently editing usage already reported for billing.
Track period boundaries, timezone, late usage, retries, and provider totals.

Use integer minor units with explicit currency scale or exact decimal arithmetic.
Currencies do not all have two decimals. Version prices and rounding rules; define
billable seats independently from invited, suspended, and free members.

## 3. Subscription Status Matrix and Grace Periods

| Provider Status | System Behavior | User Access |
|---|---|---|
| `trialing` | Trial-specific entitlement and expiry policy. | Explicit trial scope. |
| `active` | Healthy subscription; recurring payment succeeded. | Unrestricted |
| `past_due` | Apply the documented grace/dunning policy. | Configured access; retain payment recovery routes. |
| `unpaid` | Grace period expired after multiple failed retries. | Restrict to read-only or downgrade to Free tier. |
| Scheduled cancellation | Subscription may still be active with cancel-at-period-end set. | Retain paid access until the effective end, unless another policy blocks it. |
| `canceled` | Terminal provider state; distinguish immediate cancellation and refunds. | Apply terminal access policy, not an unconditional future period grant. |

Include incomplete, paused, and provider-specific states where the selected contract
uses them. A paid capability never overrides role authorization, tenant suspension,
or membership eligibility. A release flag must not become the payment source of truth.

## Failure exercise

Submit two operations for the last remaining quota unit. Exactly one may reserve it;
replaying that operation must not consume twice. Verify trial expiry, scheduled versus
immediate cancellation, and a seat change while invitations are accepted concurrently.
