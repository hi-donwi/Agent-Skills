# Flag Evaluation Patterns and Architecture

## 1. Fast Local Evaluation vs Remote Network Calls

Prefer bounded local evaluation on critical paths when the provider supports it.
If only remote evaluation is available, document a timeout, cache, failure policy,
and acceptable latency. Do not invent support for a pinned SDK or mandate a paid tool.

### Architectural Blueprint

```
[Flag Provider / Config Store]
        │ (SSE / Polling / Webhook updates)
        ▼
[In-Memory Local Rule Cache] ──(Sub-millisecond eval)──▶ [Application Route / UI]
```

1. **Daemon / Background Sync:** Stream flag rules via Server-Sent Events (SSE) or poll periodically (e.g. every 30s) into an in-memory dictionary.
2. **Safe Fallback Defaults:** Define defaults and maximum stale-rule age per flag.
   A release toggle may default off; an emergency protection flag may need the opposite.
   Measure propagation before promising a kill switch disables work immediately.

```typescript
export function isFeatureEnabled(flagKey: string, context: EvaluationContext, defaultValue = false): boolean {
  try {
    const flag = flagCache.get(flagKey);
    if (!flag) return defaultValue;
    return evaluateRules(flag, context);
  } catch (err) {
    logger.warn(`Flag evaluation error for ${flagKey}, using fallback ${defaultValue}:`, err);
    return defaultValue;
  }
}
```

## 2. Deterministic Percentage Rollouts

When rolling out to a percentage of users (e.g. 20%), evaluation MUST be deterministic: the same user must consistently see the same variant across repeated page loads and devices.

### Consistent Hashing Algorithm

```typescript
import { createHash } from "node:crypto";

export function evaluatePercentage(flagKey: string, distinctKey: string, rolloutPercentage: number): boolean {
  // Combine flagKey and distinctKey to prevent correlated rollouts across different flags
  const hash = createHash("md5")
    .update(`${flagKey}:${distinctKey}`)
    .digest("hex");

  // Take first 8 chars, parse as integer modulo 100
  const bucket = parseInt(hash.substring(0, 8), 16) % 100;
  return bucket < rolloutPercentage;
}
```

## 3. Code Cleanliness: Strategy Pattern vs If/Else

Avoid scattering `if (isEnabled("new-checkout"))` across 20 files. Encapsulate variations behind a polymorphic interface or factory:

```typescript
export interface CheckoutService {
  processOrder(order: Order): Promise<OrderResult>;
}

export function createCheckoutService(context: EvaluationContext): CheckoutService {
  if (isFeatureEnabled("v2-checkout-pipeline", context, false)) {
    return new V2CheckoutService();
  }
  return new LegacyCheckoutService();
}
```

When retiring the flag, delete `LegacyCheckoutService` and replace the factory with direct instantiation of `V2CheckoutService`.

## Failure exercise

Stop configuration updates and exercise a kill switch with a stale cache. Confirm
the documented fallback and maximum staleness behavior. Authorization and commercial
entitlement checks must still execute regardless of the selected branch.
