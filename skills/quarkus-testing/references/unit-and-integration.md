# Unit and integration tests

Load when writing the tests themselves: what each layer tests, and why PostgreSQL rather than H2.

## Unit tests

```java
class VendorServiceTest {

    private final VendorRepository repo = mock(VendorRepository.class);
    private final VendorService service = new VendorService(repo);

    @Test
    void rejectsAlreadyRegisteredTaxId() {
        when(repo.findByTaxId("012345678901234"))
                .thenReturn(Optional.of(new Vendor("PT ABC")));

        var request = new CreateVendorRequest("PT XYZ", "012345678901234", COMPANY);

        assertThatThrownBy(() -> service.create(request))
                .isInstanceOf(ValidationException.class)
                .extracting("code").isEqualTo(ErrorCode.VENDOR_TAX_ID_DUPLICATE);
    }

    @Test
    void savesVendorWithUniqueTaxId() { ... }
}
```

This is the second reason for rejecting Panache active record: a static
`Vendor.findByTaxId(...)` cannot be mocked without PowerMock. Constructor injection makes
services testable in milliseconds.

**Test names describe behaviour**, not the method: `rejectsAlreadyRegisteredTaxId`, not
`testCreate2`. The test name is what someone reads when CI goes red.

## Integration tests

```java
@QuarkusTest
class VendorResourceIT {

    @Test
    void createReturns201WithLocation() {
        given()
            .contentType(JSON)
            .auth().oauth2(committeeToken())
            .body("""
                  {"name":"PT XYZ","taxId":"012345678901234","type":"COMPANY"}
                  """)
        .when()
            .post("/api/v1/catalog/vendors")
        .then()
            .statusCode(201)
            .header("Location", matchesPattern(".*/api/v1/catalog/vendors/\\d+"))
            .body("name", equalTo("PT XYZ"));
    }

    @Test
    void duplicateTaxIdReturns422WithStableCode() {
        // ...
        .then().statusCode(422).body("code", equalTo("VENDOR_TAX_ID_DUPLICATE"));
    }
}
```

`*IT` classes run under Failsafe (`./mvnw verify`); `*Test` under Surefire (`./mvnw test`).

### Real PostgreSQL, not H2

```properties
%test.quarkus.datasource.db-kind=postgresql
# Dev Services starts the container automatically — do not set jdbc.url in the test profile
```

H2 differs from PostgreSQL exactly where it matters here: `NUMERIC` precision, date
functions, `TIMESTAMPTZ`, window functions for reporting, and `CREATE INDEX CONCURRENTLY`. A
test that passes on H2 and fails in production is worse than no test — it grants false
confidence.

Containers are shared across the run via `QuarkusTestResourceLifecycleManager`, not started
per class.
