# Choosing the type, and how failure travels

Load when deciding between a record and a class, whether a result is `Optional` or an
exception, and which exception that should be.

### Record or class?

**Record** for anything carrying data without identity: DTOs, parameter objects, return
values, events. This is the default.

**Class** only when mutable identity is required (a JPA entity) or the behaviour does not
fit a record.

```java
public record CreateVendorRequest(
        @NotBlank @Size(max = 200) String name,
        @NotBlank @Pattern(regexp = "\\d{15,16}") String taxId,
        @NotNull VendorType type) {}
```

A record may use a compact constructor for normalisation — but business validation stays in
the service:

```java
public record PageRequest(int page, int size, String sortField, String sortDir) {
    public PageRequest {
        if (page < 0) page = 0;
        size = Math.clamp(size, 1, 200);      // server-enforced cap
    }
}
```

### `Optional` or an exception?

| Situation | Use |
|---|---|
| "Look it up, it may not exist" — an ordinary outcome | `Optional<T>` |
| "Fetch by an ID that should exist" — absence is wrong | `throw NotFoundException` |
| An empty collection | `List.of()` — **never** `null` |

`Optional` is a **return type** only. Not a field, not a parameter.

```java
public Optional<Vendor> findByTaxId(String taxId) { ... }        // right
public Vendor getById(Long id) { ... }                          // right, throws if absent
public void update(Long id, Optional<String> name) { ... }      // wrong
```

### Which exception?

Three, all extending `AppException`, all carrying an `ErrorCode`:

```java
throw new NotFoundException(ErrorCode.VENDOR_NOT_FOUND, "vendor id=" + id);
throw new ValidationException(ErrorCode.VENDOR_TAX_ID_DUPLICATE, "taxId=" + taxId);
throw new ConflictException(ErrorCode.ORDER_ALREADY_APPROVED, "id=" + id);
```

`ErrorCode` is an enum that is **stable forever** — the frontend branches on it. The message
may change; the code may not.

Exception messages target the **developer** and carry debugging context (IDs, values), but
never sensitive data (passwords, confidential prices, document contents).

---
