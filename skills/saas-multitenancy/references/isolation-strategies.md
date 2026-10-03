# Multi-Tenancy Data Isolation Strategies

## 1. Architectural Models

| Model | Mechanism | Pros | Cons | Best for |
|---|---|---|---|---|
| **Pooled (Row-Level)** | Shared DB and schema; tenant-owned tables have `tenant_id`. Partitioning via PostgreSQL RLS or query filters. | Lowest cost, easiest schema migrations, maximum resource utilization. | Risk of cross-tenant leak if a query misses `tenant_id`; noisy neighbors. | Early-to-growth SaaS, B2B mid-market, high tenant count. |
| **Schema-per-tenant** | Shared DB instance, separate schema and role grants. | Logical separation and tenant-specific schema options. | Repeated migrations; unsafe search paths; restore complexity; shared capacity. | Requirements that justify additional operations. |
| **Database-per-tenant** | Separate database and scoped credentials. | Stronger persistence boundary and tenant-level recovery. | Shared hosts, caches, workers, and control planes can still leak or contend. | Contractual isolation or recovery requirements. |

## 2. Row-Level Security (PostgreSQL RLS)

RLS adds database-enforced checks; it does not replace verified application scope or
least privilege. Superusers and BYPASSRLS roles bypass it even with FORCE RLS. Owners
normally bypass it unless forced. Integrity constraints can expose information, and
TRUNCATE is not row-scoped. Restrict grants, privileged functions, and administration.

```sql
-- 1. Enable RLS on table
ALTER TABLE documents ENABLE ROW LEVEL SECURITY;
ALTER TABLE documents FORCE ROW LEVEL SECURITY;

-- 2. Define policy tied to connection session variable
CREATE POLICY tenant_isolation_policy ON documents
  FOR ALL
  USING (tenant_id = NULLIF(current_setting('app.current_tenant_id', true), '')::uuid)
  WITH CHECK (tenant_id = NULLIF(current_setting('app.current_tenant_id', true), '')::uuid);
```

### Application Connection Setup

Use one explicit transaction on one checked-out connection. A parameterized SELECT
set_config is appropriate; `SET LOCAL ... = $1` is not a bindable SQL statement.

```sql
BEGIN;
SELECT set_config('app.current_tenant_id', $1, true);
-- Execute all scoped operations on this connection, using bound parameters.
COMMIT;
```

On any failure, ROLLBACK before release; discard a connection whose rollback fails.
The `true` argument scopes the setting to the transaction. Without BEGIN, the setting
expires at the end of the SELECT statement. Do not use session-level SET in a pool.
This example requires integration tests against the target PostgreSQL version.

Enforce tenant-consistent relationships with a referenced `UNIQUE(tenant_id, id)`
and `FOREIGN KEY(tenant_id, parent_id) REFERENCES parents(tenant_id, id)`.
Inventory global identity and shared reference tables rather than forcing tenant IDs
onto data whose intentional ownership is global. Application roles must not be able
to supply arbitrary verified context or execute untrusted SQL.

## 3. Storage and Cache Isolation

1. **Redis / Memcached:** Always prefix cache keys with tenant namespace:
   `tenant:{tenantId}:{resource}:{id}` (e.g., `tenant:42:user:101`). Never store bare IDs in global cache keys.
2. **Object Storage (S3 / Cloud Storage):**
   Structure bucket paths: `s3://bucket-name/tenants/{tenantId}/{category}/{fileId}`.
   Generate pre-signed URLs scoped strictly to tenant-prefixed keys.
3. **Search Indexes (Elasticsearch, Meilisearch):**
   Either index-per-tenant (`tenants_{tenantId}_docs`) or mandatory filter query in every search request (`{ filter: "tenant_id = '42'" }`).
4. **Message Queues / Background Jobs:**
   Every job payload must serialize `tenantId`. Worker threads must re-establish the tenant execution context before processing.

## 4. Noisy-Neighbor Mitigation

- Rate-limit aggregate API consumption by tenant; add per-IP limits for abuse defense.
- Set per-tenant concurrency limits on heavy async jobs (e.g. max 5 concurrent report generations per tenant).
- Attribute expensive work to tenants using bounded-cardinality metrics or controlled
  logs; do not create an unbounded tenant label in every time series.

## Source and failure exercise

[PostgreSQL row security](https://www.postgresql.org/docs/current/ddl-rowsecurity.html)
defines policy, privilege bypass, and constraint limitations. Test with two tenants,
missing context, a failed transaction, and immediate pool reuse under a non-owner
runtime role. No row or write may inherit the previous tenant's scope.
