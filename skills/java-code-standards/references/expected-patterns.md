# Expected patterns

Load for the worked form of each pattern this skill expects: control flow, state, SQL,
money, and logging.

## Expected patterns

### Early returns, not nesting

```java
// WRONG — four levels deep
public void process(Order p) {
    if (p != null) {
        if (p.status == DRAFT) {
            if (p.amount != null) {
                if (p.amount.compareTo(BigDecimal.ZERO) > 0) {
                    send(p);
                }
            }
        }
    }
}

// RIGHT — flat, every rejection states its reason
public void process(Order p) {
    Objects.requireNonNull(p, "order");
    if (p.status != DRAFT) {
        throw new ConflictException(ErrorCode.ORDER_NOT_DRAFT, "id=" + p.id);
    }
    if (p.amount == null || p.amount.signum() <= 0) {
        throw new ValidationException(ErrorCode.AMOUNT_INVALID, "id=" + p.id);
    }
    send(p);
}
```

### Pattern-matching switch for state

```java
String label = switch (status) {
    case DRAFT               -> "Draft";
    case SUBMITTED           -> "Awaiting approval";
    case APPROVED            -> "Approved";
    case REJECTED, CANCELLED -> "Not proceeding";
};
```

A switch over an enum without `default` makes the compiler flag any newly added enum
constant that is not handled. **Do not add a `default`** just to satisfy the compiler —
that throws away the safety net.

### Text blocks for SQL

```java
private static final String SQL_SUMMARY = """
        SELECT order_type, COUNT(*) AS total, SUM(amount) AS amount
        FROM order
        WHERE transaction_date BETWEEN ?1 AND ?2
          AND deleted_at IS NULL
        GROUP BY order_type
        """;
```

### Money

**`BigDecimal`, always.** Never `double` or `float`.

```java
BigDecimal total = price.multiply(BigDecimal.valueOf(quantity))
                        .setScale(2, RoundingMode.HALF_UP);

// compare with compareTo, not equals
if (amount.compareTo(BigDecimal.ZERO) > 0) { ... }
```

`equals` on `BigDecimal` takes scale into account: `new BigDecimal("1.0")` does not equal
`new BigDecimal("1.00")`. This is a comparison bug that is easy to miss in review.

### Logging

```java
private static final Logger log = Logger.getLogger(VendorService.class);

log.infof("vendor created id=%d taxId=%s", id, maskTaxId(taxId));
```

Parameterised, not concatenated. Never `System.out`. Never sensitive data.

---
