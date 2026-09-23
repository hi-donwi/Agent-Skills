# Transactions, N+1, and report queries

Load when deciding a transaction boundary, chasing a slow endpoint, or writing a query that
feeds a report.

## Transactions

`@Transactional` **only in services**. One transaction equals one business operation.

```java
// WRONG — an HTTP call holds the DB connection for its whole timeout
@Transactional
public void submit(Long id) {
    var p = order.findById(id);
    p.status = SUBMITTED;
    notificationClient.send(p);
}

// RIGHT — commit first, side effects after
public void submit(Long id) {
    var snapshot = changeStatus(id);        // @Transactional
    notificationClient.send(snapshot);      // outside
}

@Transactional
OrderSnapshot changeStatus(Long id) { ... }
```

Read-only: `@Transactional(TxType.SUPPORTS)`.

---

## N+1 — a bug, not merely slow

Enable it in dev and watch:

```properties
%dev.quarkus.hibernate-orm.log.sql=true
```

One request printing 50 SELECTs is a finding, not a coincidence.

```java
// WRONG — 1 + N queries
var list = orderRepo.listAll();
list.forEach(p -> use(p.vendor.name));   // one SELECT per row

// RIGHT — one query
var list = orderRepo.find("""
        select p from Order p
        join fetch p.vendor
        where p.deletedAt is null
        """).page(page).list();
```

All associations are `LAZY`; load explicitly with `join fetch` where needed. `EAGER` moves
the problem rather than removing it — it loads unused data on every other query.

## Report queries

Aggregation happens in the **database**, not in Java.

```java
// WRONG — loading 500,000 rows into memory to sum them
var all = orderRepo.listAll();
var total = all.stream().map(p -> p.amount).reduce(ZERO, BigDecimal::add);

// RIGHT
@ApplicationScoped
public class SummaryRepository {
    @Inject EntityManager em;

    public List<SummaryRow> summaryByType(LocalDate from, LocalDate to) {
        return em.createNativeQuery("""
                SELECT order_type, COUNT(*), SUM(amount)
                FROM order
                WHERE transaction_date BETWEEN :from AND :to AND deleted_at IS NULL
                GROUP BY order_type
                """, SummaryRow.class)
            .setParameter("from", from)
            .setParameter("to", to)
            .getResultList();
    }
}
```

Always parameters (`?1`, `:name`), **never** string concatenation of user input. Dynamic
`ORDER BY` uses an allowlist — see `quarkus-security`.
