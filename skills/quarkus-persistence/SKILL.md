---
name: quarkus-persistence
description: >-
  Work with data in Quarkus: JPA entities, PanacheRepository, forward-only Flyway migrations
  that are safe on populated tables, PostgreSQL schema conventions, audit columns, soft
  delete, transaction boundaries, avoiding N+1, indexing, and aggregate queries for reports.
  Use when creating or changing an entity, writing a migration, writing a query, fixing a
  slow request or N+1, deciding a transaction boundary, or designing a new table. Do not use
  for API response shape (rest-api-contract), large file exports (bulk-reporting-export), or
  domain business rules (the organisation domain skill under context/skills/).
metadata:
  pack: java
  keywords: entity, panache, repository, flyway, migration, query, transaction, index, n+1, database, sql, jpa, hibernate, schema, table, column, soft delete, audit column, postgres
---

# Quarkus Persistence

## Overview

Full rules: `.agents/standards/java/database.md`. This is the workflow and the patterns.

## When to use
- Creating or changing an entity or table
- Writing a Flyway migration
- Writing or optimising a query
- A slow endpoint suspected of being a data problem
- Deciding where `@Transactional` goes

---

## Process

1. **Migration first.** The schema is the source of truth and the entity follows it, never
   the other way round. Forward-only; no edit to a migration that has run anywhere.
2. **The entity mirrors the table.** It does not create it. `@Enumerated(EnumType.STRING)`
   always — `ORDINAL` stores the enum's position in the source, so inserting one value in
   the middle silently changes the meaning of every existing row.
3. **`PanacheRepository`, not active record.** A repository can be mocked, which is what
   lets a service be tested in milliseconds without a database.
4. **Audit columns come from a `@MappedSuperclass`**, set by `@PrePersist`/`@PreUpdate`,
   not by each caller remembering.
5. **Own the transaction at the service boundary.** `@Transactional` belongs on the service
   method that represents one unit of work — not on a repository, not on a resource.
6. **Treat N+1 as a bug, not as slowness.** It passes every test with ten rows and fails in
   production with ten thousand. Fetch what the caller will read.
7. **Let the database do set work.** Sums, counts, group-bys and paging belong in SQL, not
   in a loop over an entity list.

A migration that is safe on an empty database can still lock a populated one for minutes.
Before writing one against real data, read `references/migrations.md`.

## Verification
- [ ] Migration exists before the entity change
- [ ] New columns are nullable or backfilled
- [ ] `@Transactional` is on the service, not the resource
- [ ] Collection queries cannot N+1
- [ ] Report aggregations run in SQL, not in Java

## Red flags

| Pitfall | Consequence |
|---|---|
| `generation=update` | Hibernate alters the production schema. Always `none`. |
| `EnumType.ORDINAL` | Inserting an enum value changes the meaning of old data |
| `float`/`double` for money | Rounding errors in financial reports |
| `TIMESTAMP` without a zone | Ambiguous when the server's zone changes |
| Entity returned as JSON | Internal columns leak, `LazyInitializationException` |
| Editing a merged migration | Checksum failure, startup dies in staging |
| A transaction wrapping an HTTP call | Connection pool exhausted under load |
| No index on a filter column | Sequential scan; fine in a demo, fatal in production |

## References
- `references/entities-and-repositories.md` - the worked migration/entity/repository/audit example
- `references/migrations.md` - changes that are safe against a populated table
- `references/transactions-and-queries.md` - transaction boundaries, N+1, report queries
