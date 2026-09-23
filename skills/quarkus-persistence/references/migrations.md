# Migrations that are safe on real data

Load before writing a migration that touches a populated table.

## Migrations that are safe on real data

The `order` table will be large. What locks:

```sql
-- WRONG — rewrites the whole table
ALTER TABLE order ADD COLUMN currency CHAR(3) NOT NULL DEFAULT 'USD';

-- RIGHT — three steps
ALTER TABLE order ADD COLUMN currency CHAR(3);
UPDATE order SET currency = 'USD' WHERE currency IS NULL;
ALTER TABLE order ALTER COLUMN currency SET NOT NULL;
```

Indexes on large tables:

```sql
-- flyway:executeInTransaction=false
CREATE INDEX CONCURRENTLY ix_order_date ON order (transaction_date);
```

Rules:
- Timestamp naming: `V<YYYYMMDD>_<HHmm>__<description>.sql` — sequential numbers collide as
  soon as two developers write a migration on the same day.
- **Forward-only.** Mistakes are corrected by a new migration.
- **Merged files are never edited** — Flyway's checksum will refuse startup in every
  environment that already ran it.
- Test against a populated dump, not an empty database.
- Backward-compatible by one release: do not drop a column in the same release that stops
  using it, so an application rollback stays possible.

---
