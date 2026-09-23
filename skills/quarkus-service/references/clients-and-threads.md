# REST clients, virtual threads, and lifting demo code

Load when calling another service, choosing a threading model, or turning a prototype into production code.

## REST clients between services

```java
@RegisterRestClient(configKey = "export-service")
@Path("/api/v1/export")
public interface ExportClient {
    @POST Response submit(ExportRequest request);
}
```

```properties
quarkus.rest-client.export-service.url=${EXPORT_SERVICE_URL}
quarkus.rest-client.export-service.connect-timeout=5000
quarkus.rest-client.export-service.read-timeout=30000
```

**Timeouts must be explicit.** An unbounded default means one slow service exhausts its
caller's thread pool until the caller dies too.

Add fault tolerance where a call is allowed to fail:

```java
@Retry(maxRetries = 2, delay = 500)
@Timeout(value = 30, unit = ChronoUnit.SECONDS)
@Fallback(fallbackMethod = "markPending")
Response submit(ExportRequest request);
```

Retry only **idempotent** operations. Retrying a `POST` that creates data produces
duplicates.

## Virtual threads

Java 21 provides virtual threads, but this is not a "go faster" switch.

- Apply `@RunOnVirtualThread` **per endpoint** where the work is I/O-bound (many JDBC/HTTP
  calls).
- **Do not** enable it globally.
- Do not use `synchronized` around a blocking call inside one — the carrier thread gets
  pinned and the benefit disappears. Use `ReentrantLock`.
- It does not help CPU-bound work (PDF generation, in-memory aggregation).

## Lifting demo code to production

The gap between `.local/demo` and the standards:

| Demo | Production |
|---|---|
| `com.demo.tender` | `com.example.product` |
| Entities returned as JSON | `record` DTOs |
| Queries in resources | Repositories |
| `PanacheEntityBase` active record | `PanacheRepository` |
| `cors.origins=*` | Per-environment allowlist |
| Password in `application.properties` | `${ENV_VAR}` |
| `ConcurrentHashMap` sessions | Redis |
| PBKDF2 | Argon2id |
| No API version | `/api/v1/` |
| Raw string errors | RFC 9457 problem+json |
| H2 for tests | Testcontainers PostgreSQL |
| No correlation ID | MDC `requestId` |

The demo is a proof of concept that worked, not a foundation. Copying its patterns into a
large API multiplies every gap in that table once per endpoint.
