# What must be tested, what need not be, and fixtures

Load when deciding whether something needs a test, and when building the data it runs against.

## Tests that must exist

| Change | Test |
|---|---|
| New endpoint | Integration: success, 400, 401/403, 404 |
| Business rule | Unit: happy path **and every rejection** |
| Bug fix | A test that **fails before the fix** |
| Migration | Run against a populated dump |
| Authorisation change | The wrong role is rejected |

### Bug fixes: red first

Write the test, run it, **confirm it is red**, then fix. If the test cannot be made red, the
bug is not yet understood — and what you "fixed" may not be the cause.

### Authorisation tests are not optional

```java
@Test
void supplierCannotViewListPrice() {
    given().auth().oauth2(supplierToken())
    .when().get("/api/v1/orders/{id}/list-price", id)
    .then().statusCode(403);
}
```

The rule "a supplier must not see a confidential list price before it is published" is only
real if a test goes red when someone loosens it.

## What does not need tests

Testing time is finite.

- Getters/setters, `record` accessors
- The framework itself (that Panache can persist)
- Trivial mappers with no logic
- Configuration without branching

## Fixtures

```java
public final class VendorFixture {
    public static Vendor active(String name) { ... }
    public static CreateVendorRequest request() { ... }
}
```

In `src/test/java/.../fixture/`. Not copy-pasted literals across 40 tests — when a new
required field appears, those 40 tests have to be edited one at a time.

Test data uses obviously fictional names: `PT Example One`, tax ID `000000000000000`.
**Never** a production dump or real client data.
