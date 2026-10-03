# Tenant Context Resolution and Propagation

## 1. Resolution Order

Resolve tenant identity early in the request pipeline before any data access occurs:

1. **Subdomain or Host:** Resolve registered domains through a controlled mapping; validate proxy and host configuration.
2. **Authenticated JWT Claims:** Verify issuer, audience, signature, and expiry; confirm current membership or documented revocation policy.
3. **HTTP Header:** `X-Tenant-ID` or `Tenant-Slug`. Only for internal service-to-service calls or API-key driven developer endpoints. Never trust client-supplied headers without cross-referencing user membership.
4. **Path Parameter:** `/api/v1/orgs/{orgId}/projects`. A requested organization still requires current actor authorization.

Define one canonical resolution rule and reject conflicting sources. Never silently
fall back to a default tenant. Public signup uses an explicitly separate unscoped
route rather than weakening tenant-owned service boundaries.

## 2. In-Process Context Propagation

Use explicit immutable context parameters or runtime-scoped storage appropriate to
the stack. Neither is mandatory. Async runtimes require async-aware context; raw
thread-locals must not survive thread reuse or cross coroutine boundaries.

### Node.js / TypeScript (`AsyncLocalStorage`)

```typescript
import { AsyncLocalStorage } from "node:async_hooks";

export interface TenantContext {
  tenantId: string;
  tenantSlug: string;
  userId: string;
}

export const tenantStorage = new AsyncLocalStorage<TenantContext>();

export function getTenantContext(): TenantContext {
  const ctx = tenantStorage.getStore();
  if (!ctx) {
    throw new Error("Illegal access: Tenant context is not established for this execution frame");
  }
  return ctx;
}
```

### Express Middleware (Illustrative)

The application supplies a typed verifiedTenantContext after authentication and
membership verification. This example is not a drop-in Fastify plugin.

```typescript
app.use((req, res, next) => {
  // Illustrative: authentication and current membership verification run first.
  const context = req.verifiedTenantContext;
  if (!context) return res.status(403).end();
  tenantStorage.run(context, () => {
    next();
  });
});
```

## 3. Query Scoping Rules

Every repository or query builder layer must enforce tenant boundaries:

1. **ORM Filters:** Verify the pinned ORM's coverage for reads, writes, joins, nested operations, and raw SQL. Do not assume a filter covers every code path.
2. **Bulk Queries and Aggregations:** Always include `tenant_id` in the grouping and indexing keys:
   `CREATE INDEX idx_orders_tenant_created ON orders (tenant_id, created_at DESC);`
3. **Unique Constraints:** Scope tenant-owned identifiers with `UNIQUE(tenant_id, slug)`.
   Global user identities may intentionally have global uniqueness; document ownership.
4. **Jobs:** Resolve a trusted job record, validate its tenant and actor or service
   permissions, and construct fresh context. Do not trust queue fields as authority.
5. **Failure exercise:** A forged header or stale membership must deny access; a
   suspended tenant must not regain access through an old job or cached context.
